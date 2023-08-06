import json

# from sqlalchemy.event import listen
from opentelemetry.instrumentation.utils import _generate_sql_comment
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from sqlalchemy import event
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor, EngineTracer

from fastapialchemycollector import PlanCollectType
from fastapialchemycollector.consts import (
    METIS_DO_NOT_TRACK_COMMENT,
    METIS_STATEMENT_SPAN_ATTRIBUTE,
    METIS_QUERY_SPAN_NAME, METIS_PLAN_SPAN_ATTRIBUTE,
)
from fastapialchemycollector.instruments import EXPLAIN_SUPPORTED_STATEMENTS
from opentelemetry.trace import Span

INSTRUMENTING_LIBRARY_VERSION = '0.30b1'


def add_quote_to_value_of_type_string(value):
    if isinstance(value, str):
        new_value = str(value).replace("'", "''")
        return "'{}'".format(new_value)  # pylint: disable=consider-using-f-string
    return value


def fix_sql_query(sql, params):
    """without the fix the query is not working because string is not quoted"""
    fixed_param = params
    if isinstance(params, dict):
        fixed_param = {
            key: add_quote_to_value_of_type_string(value)
            for key, value in params.items()
        }

    return sql % fixed_param


class MetisSQLAlchemyInstrumentor(SQLAlchemyInstrumentor):
    def _instrument(self, **kwargs):
        self.plan_collection_option = kwargs.get(
            "plan_collection_option",
            PlanCollectType.ESTIMATED,
        )
        self.exporter_tracer: EngineTracer = super()._instrument(enable_commenter=True, **kwargs)

        self.tracer_provider = kwargs.get('trace_provider')

        self.exporter_tracer.tracer = trace.get_tracer(
            "metis",
            INSTRUMENTING_LIBRARY_VERSION,
            tracer_provider=self.tracer_provider,
        )

        engine = kwargs.get("engine")

        def handle_error(context):
            span = getattr(context.execution_context, "_metis_span", None)

            if span is None:
                return

            if span.is_recording():
                # If the exception means the operation results in an
                # error state, you can also use it to update the span status.
                span.set_status(
                    Status(
                        StatusCode.ERROR,
                        str(context.original_exception),
                    ),
                )
                span.record_exception(context.original_exception)

            span.end()

        event.listen(engine, "before_cursor_execute", self.before_query_hook, retval=True)
        event.listen(engine, "handle_error", handle_error)

    def before_query_hook(  # pylint: disable=too-many-arguments, unused-argument
            self,
            conn,
            cursor,
            statement,
            parameters,
            context,
            executemany,
    ):
        if statement.startswith(METIS_DO_NOT_TRACK_COMMENT):
            return statement, parameters

        current_span = context._otel_span
        if current_span.is_recording():
            interpolated_statement = fix_sql_query(statement, parameters)

            current_span.set_attribute(
                METIS_STATEMENT_SPAN_ATTRIBUTE,
                interpolated_statement,
            )

            if self.plan_collection_option == PlanCollectType.ESTIMATED:
                if conn.dialect.name != "postgresql":
                    raise Exception(
                        "Plan collection is only supported for PostgreSQL",
                    )
                if any(
                        statement.upper().startswith(prefix)
                        for prefix in EXPLAIN_SUPPORTED_STATEMENTS
                ):
                    result = conn.exec_driver_sql(
                        METIS_DO_NOT_TRACK_COMMENT
                        + "explain (verbose, costs, summary, format JSON) "
                        + statement,
                        parameters,
                    )
                    res = result.fetchall()
                    if not res:
                        raise Exception("No plan found")
                    current_span.set_attribute(
                        METIS_PLAN_SPAN_ATTRIBUTE,
                        json.dumps(res[0][0][0]),
                    )

        return statement, parameters

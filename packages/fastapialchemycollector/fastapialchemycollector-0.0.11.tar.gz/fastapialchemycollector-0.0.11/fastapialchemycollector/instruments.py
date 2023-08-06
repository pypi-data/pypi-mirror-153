from __future__ import absolute_import, division, print_function, unicode_literals

import json
import os
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import Status, StatusCode, TracerProvider, Span
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry import trace
from opentelemetry.semconv.trace import SpanAttributes
from sqlalchemy.event import listen

from fastapialchemycollector.consts import (
    METIS_REQUEST_SPAN_ATTRIBUTE_IDENTIFIER,
    METIS_DO_NOT_TRACK_COMMENT,
    METIS_QUERY_SPAN_NAME,
    METIS_STATEMENT_SPAN_ATTRIBUTE,
    METIS_PLAN_SPAN_ATTRIBUTE,
)
from fastapialchemycollector.exporters.file_exporter import MetisFileExporter
from fastapialchemycollector.exporters.remote_exporter import MetisRemoteExporter
from fastapialchemycollector.plan_collect_type import PlanCollectType

FILE_NAME = "metis-log-collector.log"

os.environ[
    "OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SERVER_REQUEST"
] = "content-type,custom_request_header"
os.environ[
    "OTEL_INSTRUMENTATION_HTTP_CAPTURE_HEADERS_SERVER_RESPONSE"
] = "content-type,content-length,custom_request_header"

EXPLAIN_SUPPORTED_STATEMENTS = (
    "SELECT",
    "INSERT",
    "UPDATE",
    "DELETE",
)


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


def _normalize_vendor(vendor):
    """Return a canonical name for a type of database."""
    if not vendor:
        return "db"  # should this ever happen?

    if "sqlite" in vendor:
        return "sqlite"

    if "postgres" in vendor or vendor == "psycopg2":
        return "postgresql"

    return vendor


def collect_logs(
    app,
    engine,
    file_name=None,
    plan_collection_option=PlanCollectType.ESTIMATED,
    api_key=None,
    endpoint=None,

):
    if not file_name and not endpoint:
        file_name = os.getenv("METIS_LOG_FILE_NAME", FILE_NAME)

    metis = MetisInstrumentor(plan_collection_option)

    if file_name:
        metis.add_processor(BatchSpanProcessor(MetisFileExporter(file_name)))

    if bool(endpoint) != bool(api_key):
        raise ValueError("Both endpoint and api_key must be provided")

    if endpoint is not None:
        metis.add_processor(BatchSpanProcessor(MetisRemoteExporter(endpoint, api_key)))

    metis.instrument_app(app, engine)


# pylint: disable=too-few-public-methods
class MetisInstrumentor:
    def __init__(self, plan_collection_option):
        self.tracer_provider = TracerProvider(
            resource=Resource.create({SERVICE_NAME: "api-service"}),
        )
        self.tracer = trace.get_tracer(
            "metis",
            "",
            tracer_provider=self.tracer_provider,
        )
        self.plan_collection_option = plan_collection_option

    def add_processor(self, processor):
        self.tracer_provider.add_span_processor(processor)

    def instrument_app(self, app, engine):
        def request_hook(
            span: Span,
            message: dict,
        ):  # pylint: disable=unused-argument
            if span and span.is_recording():
                span.set_attribute(METIS_REQUEST_SPAN_ATTRIBUTE_IDENTIFIER, True)

        FastAPIInstrumentor().instrument_app(
            app,
            tracer_provider=self.tracer_provider,
            server_request_hook=request_hook,
            excluded_urls='favicon'
        )

        engine = engine.sync_engine if hasattr(engine, 'sync_engine') and engine.sync_engine is not None else engine
        from fastapialchemycollector.alchemy_instrumentation import MetisSQLAlchemyInstrumentor
        result = MetisSQLAlchemyInstrumentor().instrument(
            engine=engine,
            trace_provider=self.tracer_provider,
        )

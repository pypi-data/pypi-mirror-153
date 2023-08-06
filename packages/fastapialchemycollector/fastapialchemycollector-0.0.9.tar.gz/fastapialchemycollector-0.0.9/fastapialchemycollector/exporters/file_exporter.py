from __future__ import division, absolute_import, print_function, unicode_literals

import json
import typing
import uuid
from datetime import datetime

import requests
from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.trace import SpanKind

from fastapialchemycollector.consts import (
    METIS_REQUEST_SPAN_ATTRIBUTE_IDENTIFIER,
    METIS_QUERY_SPAN_NAME,
    METIS_STATEMENT_SPAN_ATTRIBUTE,
    METIS_PLAN_SPAN_ATTRIBUTE,
)


class MetisFileExporter(SpanExporter):
    def __init__(
        self,
        filename,
    ):
        self.dict = {}
        self.filename = filename

    def export(self, spans: typing.Sequence[ReadableSpan]) -> SpanExportResult:
        try:
            for span in spans:
                trace_id = span.context.trace_id

                if self.dict.get(trace_id) is None:
                    self.dict[trace_id] = []

                if METIS_STATEMENT_SPAN_ATTRIBUTE in span.attributes or \
                    METIS_REQUEST_SPAN_ATTRIBUTE_IDENTIFIER in span.attributes:
                    self.dict[trace_id].append(span)

                if not span.parent and span.kind == SpanKind.SERVER:
                    self.export_to_file(trace_id)
        except Exception as e:
            print(e)
            pass

        return SpanExportResult.SUCCESS

    def export_to_file(self, trace_id):
        spans = self.dict[trace_id]
        del self.dict[trace_id]

        parent = None
        try:
            parent = next(
                span
                for span in spans
                if not span.parent
                and METIS_REQUEST_SPAN_ATTRIBUTE_IDENTIFIER in span.attributes
            )
        except StopIteration:
            pass

        # for now, we don't track sql queries that not under request span
        if not parent:
            return

        spans.remove(parent)

        if not spans:
            return

        data = {
            "logs": list(
                map(
                    lambda x: {
                        "_uuid": str(uuid.uuid1()),
                        "query": x.attributes.get(METIS_STATEMENT_SPAN_ATTRIBUTE),
                        "dbEngine": x.attributes.get(SpanAttributes.DB_SYSTEM),
                        "date": datetime.utcnow().isoformat(),
                        "plan": json.loads(x.attributes.get(METIS_PLAN_SPAN_ATTRIBUTE))
                        if x.attributes.get(METIS_PLAN_SPAN_ATTRIBUTE)
                        else None,
                    },
                    spans,
                ),
            ),
            "framework": "FastAPI",
            "path": parent.attributes.get(SpanAttributes.HTTP_TARGET, "N/A"),
            "operationType": parent.attributes.get(SpanAttributes.HTTP_METHOD, "N/A"),
            "requestDuration": (parent.end_time - parent.start_time) / 1000000,
            "requestStatus": parent.attributes.get(
                SpanAttributes.HTTP_STATUS_CODE,
                "N/A",
            ),
        }

        with open(self.filename, "a", encoding="utf8") as file:
            file.write(json.dumps(data) + "\n")


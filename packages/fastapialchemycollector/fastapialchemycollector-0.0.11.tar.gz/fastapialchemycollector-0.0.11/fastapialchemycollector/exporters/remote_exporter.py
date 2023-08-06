import json
from typing import Sequence
import logging
import requests
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult
from opentelemetry.trace import Span
import logging
from fastapialchemycollector.consts import METIS_REQUEST_SPAN_ATTRIBUTE_IDENTIFIER, METIS_QUERY_SPAN_NAME, \
    METIS_STATEMENT_SPAN_ATTRIBUTE
import base64

logger = logging.getLogger(__name__)

class MetisRemoteExporter(SpanExporter):
    def __init__(self, url, api_key):
        self.url = url
        self.session = requests.Session()
        self.session.headers.update(
            {"x-api-key": api_key}
        )

    def export(self, spans: Sequence[Span]) -> SpanExportResult:
        try:

            data = [json.loads(span.to_json(indent=0)) for span in spans if METIS_STATEMENT_SPAN_ATTRIBUTE in span.attributes or
                    METIS_REQUEST_SPAN_ATTRIBUTE_IDENTIFIER in span.attributes]
            if data:
                result = self.session.post(
                    url=self.url,
                    json={"base64data": base64.b64encode(json.dumps(data).encode("utf-8")).decode("utf-8")}
                )
                logger.debug(result.text)

            return SpanExportResult.SUCCESS
        except Exception as e:
            logger.error("Error exporting spans to remote: {}".format(e))
            return SpanExportResult.FAILURE

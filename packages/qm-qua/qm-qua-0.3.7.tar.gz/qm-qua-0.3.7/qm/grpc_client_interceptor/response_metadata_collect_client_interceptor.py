"""Interceptor that collects metadata from incoming responses."""
import dataclasses
from collections import deque
from typing import Deque

from qm.grpc_client_interceptor import generic_client_interceptor
from qm.logger import logger

RECEIVED_HEADERS_MAX_SIZE = 10000


@dataclasses.dataclass
class DebugData:
    received_headers: Deque[dict] = dataclasses.field(
        default_factory=lambda: deque(maxlen=RECEIVED_HEADERS_MAX_SIZE)
    )

    def append(self, received_metadata):
        self.received_headers.append(received_metadata)


def response_metadata_collect_client_interceptor(debug_data: DebugData):
    def intercept_call(
        client_call_details, request_iterator, request_streaming, response_streaming
    ):
        def extract_response_metadata(response):
            received_metadata = {it.key: it.value for it in response.initial_metadata()}
            logger.debug("Collected response metadata: {}" % received_metadata)
            debug_data.append(received_metadata)
            return response

        return client_call_details, request_iterator, extract_response_metadata

    return generic_client_interceptor.create(intercept_call)

import contextlib
import functools
import grpc
import logging
import time

from grpc import StatusCode
from typing import Dict, cast

from grpc.aio import ServerInterceptor
from prometheus_client import (
    Counter,
    Histogram,
    REGISTRY,
    PROCESS_COLLECTOR,
    PLATFORM_COLLECTOR,
)
from prometheus_client.registry import CollectorRegistry

REGISTRY.unregister(PROCESS_COLLECTOR)
REGISTRY.unregister(PLATFORM_COLLECTOR)
REGISTRY.unregister(REGISTRY._names_to_collectors["python_gc_objects_collected_total"])

"""As ServicerContext.code() returns the integer value of the StatusCode we
want to get the enum value for it"""
STATUS_CODE_BY_INT_VALUE: Dict[int, grpc.StatusCode] = {
    cast(int, enum_field.value[0]): enum_field for enum_field in grpc.StatusCode
}


class MetricsInterceptor(ServerInterceptor):
    registry: CollectorRegistry
    request_count: Counter
    latency_seconds: Histogram

    def __init__(self, registry: CollectorRegistry = REGISTRY) -> None:
        self.request_count = Counter(
            "request_count",
            "Total number of RPCs started on the server.",
            ["grpc_service", "grpc_method", "grpc_code"],
            registry=registry,
        )
        self.latency_seconds = Histogram(
            "latency_seconds",
            "Histogram of response latency (seconds)",
            ["grpc_service", "grpc_method", "grpc_code"],
            registry=registry,
        )

    async def intercept_service(self, continuation, handler_call_details):
        service_name, method_name = self._split_service_method_names(
            handler_call_details
        )

        continuation_handler = await continuation(handler_call_details)

        if not service_name.startswith("grpc."):
            continuation_handler_class = type(continuation_handler)
            continuation_handler = continuation_handler_class(
                request_streaming=continuation_handler.request_streaming,
                response_streaming=continuation_handler.response_streaming,
                request_deserializer=continuation_handler.request_deserializer,
                response_serializer=continuation_handler.response_serializer,
                unary_unary=self._wrap_unary_response(
                    continuation_handler.unary_unary, service_name, method_name
                ),
                unary_stream=self._wrap_stream_response(
                    continuation_handler.unary_stream, service_name, method_name
                ),
                stream_unary=self._wrap_unary_response(
                    continuation_handler.stream_unary, service_name, method_name
                ),
                stream_stream=self._wrap_stream_response(
                    continuation_handler.stream_stream, service_name, method_name
                ),
            )

        return continuation_handler

    def _wrap_unary_response(self, original, service_name, method_name):
        if not original:
            return original

        @functools.wraps(original)
        async def behavior(request_or_iterator, servicer_context):
            with self._track_request(service_name, method_name, servicer_context):
                return await original(request_or_iterator, servicer_context)

        return behavior

    def _wrap_stream_response(self, original, service_name, method_name):
        if not original:
            return original

        @functools.wraps(original)
        async def behavior(request_or_iterator, servicer_context):
            with self._track_request(service_name, method_name, servicer_context):
                async for chunk in original(request_or_iterator, servicer_context):
                    yield chunk

        return behavior

    def _split_service_method_names(self, handler_call_details):
        """
        Infers the grpc service and method name from the handler_call_details.
        """

        # e.g. /package.ServiceName/MethodName
        parts = handler_call_details.method.split("/")
        if len(parts) < 3:
            return "", ""

        service_name, method_name = parts[1:3]
        return service_name, method_name

    @contextlib.contextmanager
    def _track_request(self, service_name, method_name, servicer_context):
        grpc_code = StatusCode.UNKNOWN
        start_time = time.perf_counter()
        try:
            yield
            grpc_code = StatusCode.OK
        except grpc.aio.AbortError as error:
            grpc_code = STATUS_CODE_BY_INT_VALUE.get(
                servicer_context.code(), StatusCode.UNKNOWN
            )
            logging.error(f"[{grpc_code}] {error.details()}")
            raise error

        finally:
            end_time = time.perf_counter()
            elapsed = max(end_time - start_time, 0)

            logging.info(
                f"[{grpc_code}] {service_name}/{method_name} [{elapsed * 1000:.2f}ms]"
            )
            labels = {
                "grpc_service": service_name,
                "grpc_method": method_name,
                "grpc_code": grpc_code,
            }
            self.request_count.labels(**labels).inc()
            self.latency_seconds.labels(**labels).observe(elapsed)

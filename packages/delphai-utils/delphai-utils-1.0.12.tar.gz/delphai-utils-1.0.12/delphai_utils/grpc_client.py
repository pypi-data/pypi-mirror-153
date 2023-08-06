import time
from typing import Any, Optional, Sequence, Tuple
from grpc.aio import insecure_channel as async_insecure_channel
from grpc import insecure_channel
from random import randint
import grpc


def get_grpc_client(
    Stub,
    address: str,
    is_async: bool = True,
    options: Optional[Sequence[Tuple[str, Any]]] = {},
    max_retries=4,
    use_retry_interceptor=True,
):
    sync_interceptors = (
        SyncUnaryUnaryRetryOnRpcErrorClientInterceptor(
            max_attempts=max_retries,
            sleeping_policy=ExponentialBackoff(
                init_backoff_ms=100, max_backoff_ms=1600, multiplier=2
            ),
            status_for_retry=(grpc.StatusCode.UNAVAILABLE,),
        ),
        SyncUnaryStreamRetryOnRpcErrorClientInterceptor(
            max_attempts=max_retries,
            sleeping_policy=ExponentialBackoff(
                init_backoff_ms=100, max_backoff_ms=1600, multiplier=2
            ),
            status_for_retry=(grpc.StatusCode.UNAVAILABLE,),
        ),
    )
    async_interceptors = (
        AsyncUnaryUnaryRetryOnRpcErrorClientInterceptor(
            max_attempts=max_retries,
            sleeping_policy=ExponentialBackoff(
                init_backoff_ms=100, max_backoff_ms=1600, multiplier=2
            ),
            status_for_retry=(grpc.StatusCode.UNAVAILABLE,),
        ),
    )
    if is_async:
        if use_retry_interceptor:
            channel = async_insecure_channel(address, interceptors=async_interceptors)
        else:
            channel = async_insecure_channel(address, options=options)
    else:
        channel = insecure_channel(address, options=options)
        if use_retry_interceptor:
            channel = grpc.intercept_channel(channel, *sync_interceptors)
    client = Stub(channel)
    return client


# Taken from https://github.com/grpc/grpc/issues/19514#issuecomment-531700657
class ExponentialBackoff:
    def __init__(self, *, init_backoff_ms: int, max_backoff_ms: int, multiplier: int):
        self.init_backoff = randint(0, init_backoff_ms)
        self.max_backoff = max_backoff_ms
        self.multiplier = multiplier

    def sleep(self, try_i: int):
        sleep_range = min(
            self.init_backoff * self.multiplier ** try_i, self.max_backoff
        )
        sleep_ms = randint(0, sleep_range)
        time.sleep(sleep_ms / 1000)


class RetryOnRpcErrorClientInterceptor(
    grpc.UnaryUnaryClientInterceptor, grpc.StreamUnaryClientInterceptor
):
    def __init__(
        self,
        *,
        max_attempts: int,
        sleeping_policy: ExponentialBackoff,
        status_for_retry: Optional[Tuple[grpc.StatusCode]] = None,
    ):
        self.max_attempts = max_attempts
        self.sleeping_policy = sleeping_policy
        self.status_for_retry = status_for_retry

    def _intercept_call(self, continuation, client_call_details, request_or_iterator):

        for try_i in range(self.max_attempts):
            response = continuation(client_call_details, request_or_iterator)

            if isinstance(response, grpc.RpcError):

                is_last_attempt = try_i == (self.max_attempts - 1)
                if is_last_attempt:
                    return response

                is_not_retryable_status = (
                    self.status_for_retry
                    and response.code() not in self.status_for_retry
                )
                if is_not_retryable_status:
                    return response

                self.sleeping_policy.sleep(try_i)
            else:
                return response

    def intercept_unary_unary(self, continuation, client_call_details, request):
        return self._intercept_call(continuation, client_call_details, request)

    def intercept_stream_unary(
        self, continuation, client_call_details, request_iterator
    ):
        return self._intercept_call(continuation, client_call_details, request_iterator)


class SyncUnaryUnaryRetryOnRpcErrorClientInterceptor(
    RetryOnRpcErrorClientInterceptor, grpc.UnaryUnaryClientInterceptor
):
    def intercept_unary_unary(self, continuation, client_call_details, request):
        return self._intercept_call(continuation, client_call_details, request)


class SyncUnaryStreamRetryOnRpcErrorClientInterceptor(
    RetryOnRpcErrorClientInterceptor, grpc.UnaryStreamClientInterceptor
):
    def intercept_unary_stream(self, continuation, client_call_details, request):
        return self._intercept_call(continuation, client_call_details, request)


class AsyncUnaryUnaryRetryOnRpcErrorClientInterceptor(
    RetryOnRpcErrorClientInterceptor, grpc.aio.UnaryUnaryClientInterceptor
):
    def intercept_unary_unary(self, continuation, client_call_details, request):
        return self._intercept_call(continuation, client_call_details, request)

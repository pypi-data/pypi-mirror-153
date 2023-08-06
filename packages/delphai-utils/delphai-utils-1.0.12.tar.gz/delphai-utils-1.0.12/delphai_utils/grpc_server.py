from itertools import chain
import collections.abc
from typing import Iterable, Iterator, Optional, Union, cast
import asyncio
import socket
from grpc import Server, aio
from grpc_reflection.v1alpha import reflection
from grpc_health.v1 import health, health_pb2_grpc
from grpc_health.v1.health_pb2 import _HEALTH
from delphai_utils.logging import logging
from google.protobuf.descriptor import FileDescriptor, ServiceDescriptor
from delphai_utils.gateway import start_gateway
from delphai_utils.keycloak import update_public_keys
from prometheus_client import start_http_server
import functools
from grpc.aio import AioRpcError
from grpc import StatusCode
from delphai_utils.interceptors.metrics import MetricsInterceptor
from delphai_utils.interceptors.authentication import AuthenticationInterceptor

shutdown_event = asyncio.Event()


def grpc_error(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        context = args[2]
        try:
            result = await func(*args, **kwargs)
            return result
        except AioRpcError as ex:
            await context.abort(ex.code(), ex.details())
        except Exception as ex:
            await context.abort(StatusCode.INTERNAL, str(ex))

    return wrapper


def is_port_free(host, port):
    """
    determine whether `host` has the `port` free

    From: https://www.thepythoncode.com/article/make-port-scanner-python
    """
    s = socket.socket()
    try:
        s.connect((host, port))
    except Exception:
        return True
    else:
        return False


class NoPortFoundError(Exception):
    ...


def find_free_port(start: int, host="127.0.0.1", num_tries=4) -> int:
    for port in range(start, start + num_tries):
        if is_port_free(host, port):
            return port
        else:
            logging.info(f"Port {port} already in use.")
    message = f"No free port found in range [{start}, {start + num_tries - 1}]"
    logging.error(message)
    raise NoPortFoundError(message)


def create_grpc_server(
    descriptors: Union[FileDescriptor, Iterable[FileDescriptor]],
    server: Optional[aio.Server] = None,
) -> aio.Server:
    """Configures a grpc server based on one or multiple proto file descriptors.

    A existing grpc server can be passed as configuration base. If not the
    default configured grpc.aio.Server will be used.
    """
    if not isinstance(descriptors, collections.abc.Iterable):
        descriptors = [descriptors]
    max_message_length = 512 * 1024 * 1024
    server = server or aio.server(
        options=[
            ("grpc.max_send_message_length", max_message_length),
            ("grpc.max_receive_message_length", max_message_length),
        ],
        interceptors=(
            AuthenticationInterceptor(),
            MetricsInterceptor(),
        ),
    )

    health_servicer = health.HealthServicer(experimental_non_blocking=True)
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)

    services: Iterator[ServiceDescriptor] = chain.from_iterable(
        [descriptor.services_by_name.values() for descriptor in descriptors]
    )
    service_names = [service.full_name for service in services]
    all_service_names = (
        *service_names,
        _HEALTH.full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(all_service_names, server)
    server.__dict__["descriptors"] = descriptors
    return server


def start_server(
    server: Server,
    gateway: bool = True,
    grpc_port: Optional[int] = None,
    http_port: Optional[int] = None,
    metrics_port: Optional[int] = None,
):
    """Start a grpc server including gateway and background tasks."""
    logging.info("starting grpc server...")
    if not grpc_port:
        grpc_port = find_free_port(8080)
    server.add_insecure_port(f"[::]:{grpc_port}")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(server.start())
    logging.info(f"started grpc server on port {grpc_port}")
    if not metrics_port:
        metrics_port = find_free_port(9191)
    start_http_server(metrics_port)
    logging.info(f"started metrics server on port {metrics_port}")
    try:
        if gateway:
            if "descriptors" not in server.__dict__:
                raise RuntimeError(
                    "Server instance does not include the proto file descriptors. Make sure you instantiate it with 'create_grpc_server'"
                )
            if not http_port:
                http_port = find_free_port(7070)
            gateway_task = start_gateway(
                cast(
                    Union[FileDescriptor, Iterable[FileDescriptor]],
                    server.__dict__["descriptors"],
                ),
                grpc_port,
                http_port,
            )
            loop.create_task(gateway_task)
        loop.create_task(server.wait_for_termination())
        loop.create_task(update_public_keys())
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info("stopped server (keyboard interrupt)")

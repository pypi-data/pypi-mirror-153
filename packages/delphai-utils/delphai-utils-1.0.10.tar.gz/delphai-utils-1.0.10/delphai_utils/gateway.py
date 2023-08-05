import collections.abc
from typing import Dict, Iterable, List, Union
from google.protobuf.descriptor import (
    FieldDescriptor,
    FileDescriptor,
    MethodDescriptor,
    ServiceDescriptor,
)
from google.protobuf.json_format import MessageToDict
from google.protobuf.message import Message
from grpc import Channel, StatusCode
from delphai_utils.logging import logging
from google.protobuf.descriptor_pb2 import MethodOptions
from google.api.http_pb2 import HttpRule
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from grpc.experimental.aio import insecure_channel, AioRpcError
from starlette.middleware.cors import CORSMiddleware
import os
from google.protobuf import symbol_database
from hypercorn.config import Config
from hypercorn.asyncio import serve
from urllib.parse import urlparse
from time import perf_counter
import json
from base64 import b64encode
from starlette_prometheus import metrics, PrometheusMiddleware
from delphai_utils.utils import generate_default_message
from jose.exceptions import JWTError
from delphai_utils.keycloak import decode_token, PublicKeyFetchError

supported_methods = ["get", "put", "post", "delete", "patch"]
status_map = {
    StatusCode.OK: 200,
    StatusCode.CANCELLED: 499,
    StatusCode.UNKNOWN: 500,
    StatusCode.INVALID_ARGUMENT: 400,
    StatusCode.DEADLINE_EXCEEDED: 504,
    StatusCode.NOT_FOUND: 404,
    StatusCode.ALREADY_EXISTS: 409,
    StatusCode.PERMISSION_DENIED: 403,
    StatusCode.UNAUTHENTICATED: 401,
    StatusCode.RESOURCE_EXHAUSTED: 429,
    StatusCode.FAILED_PRECONDITION: 412,
    StatusCode.ABORTED: 499,
    StatusCode.OUT_OF_RANGE: 416,
    StatusCode.UNIMPLEMENTED: 501,
    StatusCode.INTERNAL: 500,
    StatusCode.UNAVAILABLE: 503,
    StatusCode.DATA_LOSS: 420,
}


class AccessLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = perf_counter()
        response = await call_next(request)
        if response.status_code < 400:
            path = urlparse(str(request.url)).path
            end = perf_counter()
            elapsed = round((end - start) * 1000, 2)
            logging.info(
                f"[{response.status_code}] {request.method} {path} [{elapsed}ms]"
            )
        return response


async def process_grpc_request(
    descriptor: FileDescriptor,
    service_name: str,
    method: str,
    input: Message,
    channel: Channel,
    metadata: Dict = {},
):
    service = descriptor.services_by_name[service_name]
    method_descriptor = service.methods_by_name[method]
    input_prototype = symbol_database.Default().GetPrototype(
        method_descriptor.input_type
    )
    output_prototype = symbol_database.Default().GetPrototype(
        method_descriptor.output_type
    )
    method_callable = channel.unary_unary(
        f"/{service.full_name}/{method}",
        request_serializer=input_prototype.SerializeToString,
        response_deserializer=output_prototype.FromString,
    )
    response = await method_callable(
        input_prototype(**input), metadata=metadata.items()
    )
    return response


async def http_exception(request, exc):
    if "favicon.ico" in str(request.url):
        detail = "not found"
        status_code = 404
    else:
        path = urlparse(str(request.url)).path
        logging.error(f"[{exc.status_code}] {request.method} {path} - {exc.detail}")
        detail = exc.detail
        status_code = exc.status_code
    return JSONResponse(
        {"detail": detail, "status": exc.status_code}, status_code=status_code
    )


def get_http_handlers(
    descriptor: FileDescriptor, service_name: str, method: str, channel: Channel
):
    async def method_get_handler(request):
        service = descriptor.services_by_name[service_name]
        method_descriptor = service.methods_by_name[method]
        input = generate_default_message(method_descriptor.input_type)
        output = generate_default_message(method_descriptor.output_type)

        function_name = f"{service.full_name}.{method}"
        return JSONResponse(
            {"function_name": function_name, "input": input, "output": output}
        )

    async def request_handler(request: Request):
        body = {}
        if len(await request.body()) > 0:
            body = await request.json()
        input = {**request.path_params, **request.query_params, **body}
        metadata = {}
        if "Authorization" not in request.headers:
            logging.warn("no authorization header")
        else:
            authorization_header = request.headers.get("Authorization")
            if "Bearer " not in authorization_header:
                error_msg = "Authorization header has the wrong format."
                logging.error(error_msg, authorization_header)
                raise HTTPException(401, detail=error_msg)
            _, access_token = authorization_header.split("Bearer ")
            try:
                decoded_access_token = await decode_token(access_token)
            except JWTError as ex:
                error_msg = f"Error decoding the token: {ex}"
                logging.error(error_msg)
                raise HTTPException(401, detail=error_msg)
            except PublicKeyFetchError as ex:
                error_msg = f"Error fetching jwk from keycloak: {ex}"
                logging.error(error_msg)
                raise HTTPException(502, detail=error_msg)
            user = {
                "https://delphai.com/mongo_user_id": decoded_access_token.get(
                    "mongo_user_id"
                ),
                "https://delphai.com/client_id": decoded_access_token.get(
                    "mongo_client_id"
                ),
            }
            if (
                "realm_access" in decoded_access_token
                and "roles" in decoded_access_token.get("realm_access")
            ):
                roles = decoded_access_token.get("realm_access").get("roles")
                user["roles"] = roles
            if "group_membership" in decoded_access_token:
                user["groups"] = decoded_access_token["group_membership"]
            if "limited_dataset_group_name" in decoded_access_token:
                user["limited_dataset_group_name"] = decoded_access_token[
                    "limited_dataset_group_name"
                ]
            if "name" in decoded_access_token:
                user["name"] = decoded_access_token["name"]
            user_json = json.dumps(user).encode("ascii")
            user_b64 = b64encode(user_json).decode("utf-8")
            metadata = {
                "authorization": authorization_header,
                "x-delphai-user": user_b64,
            }

        try:
            raw_output = await process_grpc_request(
                descriptor, service_name, method, input, channel, metadata=metadata
            )
            output = MessageToDict(
                raw_output,
                preserving_proto_field_name=True,
                including_default_value_fields=True,
            )
            return JSONResponse(output)
        except AioRpcError as ex:
            detail = ex.details()
            grpc_status = ex.code()
            http_status_code = status_map[grpc_status]
            raise HTTPException(http_status_code, detail=detail)
        except Exception as ex:
            detail = str(ex).replace("\n", " ")
            http_status_code = 500
            raise HTTPException(http_status_code, detail=detail)

    return method_get_handler, request_handler


async def start_gateway(
    descriptors: Union[FileDescriptor, Iterable[FileDescriptor]],
    grpc_port: int,
    http_port: int = 7070,
):
    if not isinstance(descriptors, collections.abc.Iterable):
        descriptors = [descriptors]
    try:
        logging.info("starting gateway...")
        debug = (
            "DELPHAI_ENVIRONMENT" in os.environ
            and os.environ["DELPHAI_ENVIRONMENT"] == "development"
        )
        app = Starlette(debug=debug)
        app.add_exception_handler(HTTPException, http_exception)
        app.add_middleware(AccessLogMiddleware)
        app.add_middleware(PrometheusMiddleware)
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
            allow_credentials=True,
        )
        app.add_exception_handler(HTTPException, http_exception)
        app.add_route("/metrics/", metrics)
        max_length = 512 * 1024 * 1024
        client_options = [
            ("grpc.max_send_message_length", max_length),
            ("grpc.max_receive_message_length", max_length),
        ]
        channel = insecure_channel(f"localhost:{grpc_port}", options=client_options)
        config = Config()
        config.bind = [f"0.0.0.0:{http_port}"]
        for descriptor in descriptors:
            for service_name in descriptor.services_by_name:
                service_handler: ServiceDescriptor = descriptor.services_by_name[
                    service_name
                ]
                if service_handler.full_name.startswith("grpc."):
                    logging.info(f"skipping service {service_handler.name}")
                else:
                    logging.info(f"processing service {service_handler.name}")
                    for method_name in service_handler.methods_by_name.keys():
                        method_get_handler, request_handler = get_http_handlers(
                            descriptor, service_handler.name, method_name, channel
                        )
                        service_name = method_name[1:].split("/")[0].split(".")[-1]
                        app.add_route(
                            f"/{service_handler.full_name}.{method_name}",
                            route=method_get_handler,
                            methods=["get"],
                        )
                        app.add_route(
                            f"/{service_handler.full_name}.{method_name}",
                            route=request_handler,
                            methods=["post"],
                        )
                        logging.info(f"  processing {method_name}")
                        method_descriptor: MethodDescriptor = (
                            service_handler.methods_by_name[method_name]
                        )
                        method_options: MethodOptions = method_descriptor.GetOptions()
                        fields: List[FieldDescriptor] = method_options.ListFields()
                        for field in fields:
                            if field[0].full_name == "google.api.http":
                                http_rule: HttpRule = field[1]
                                for supported_method in supported_methods:
                                    http_path = getattr(http_rule, supported_method)
                                    if http_path != "":
                                        app.add_route(
                                            http_path,
                                            route=request_handler,
                                            methods=[supported_method],
                                        )
        logging.info(f"started gateway on port {http_port}")
        return await serve(app, config)
    except Exception as ex:
        logging.error(str(ex))

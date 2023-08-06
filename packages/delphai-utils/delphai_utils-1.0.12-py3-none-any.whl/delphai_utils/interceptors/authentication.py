import grpc
from jose.exceptions import JWTError
from delphai_utils.keycloak import decode_token, PublicKeyFetchError
from delphai_utils.logging import logging
from grpc.aio import Metadata, ServerInterceptor


class AuthenticationInterceptor(ServerInterceptor):
    error_message: str

    def __init__(self):
        async def abort(ignored_request, context):
            await context.abort(grpc.StatusCode.UNAUTHENTICATED, self.error_message)

        self._abort = grpc.unary_unary_rpc_method_handler(abort)

    async def intercept_service(self, continuation, handler_call_details):
        metadata: Metadata = handler_call_details.invocation_metadata
        authorization_header: str = None
        for metadatum in metadata:
            if metadatum[0] == "authorization":
                authorization_header = metadatum[1]
        if not authorization_header:
            logging.warning("authorization header not specified")
        else:
            if "Bearer " not in authorization_header:
                self.error_message = "Authorization header has the wrong format."
                logging.error(self.error_message, authorization_header)
                return self._abort
            _, access_token = authorization_header.split("Bearer ")
            try:
                await decode_token(access_token)
            except JWTError as ex:
                self.error_message = f"Error decoding the token: {ex}"
                logging.error(self.error_message)
                return self._abort
            except PublicKeyFetchError as ex:
                self.error_message = f"Error fetching jwk from keycloak: {ex}"
                logging.error(self.error_message)
                return self._abort
        return await continuation(handler_call_details)

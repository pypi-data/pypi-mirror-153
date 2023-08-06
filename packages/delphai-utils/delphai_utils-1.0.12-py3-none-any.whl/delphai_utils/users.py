from typing import Dict, List, Tuple, Union
from grpc.aio import ServicerContext
from delphai_utils.keycloak import decode_token
import asyncio
import nest_asyncio
import json
from base64 import b64decode

nest_asyncio.apply()


def get_user(context: ServicerContext) -> Dict:
    """
    Get x-delphai-user information.
    :param grpc.aio.ServicerContext context: context passed to grpc endpoints
    :raises: KeyError
    :return x-delphai-user dictionary.
      More information: https://wiki.delphai.dev/wiki/Authorization
    :rtype: Dict
    """

    metadata = dict(context.invocation_metadata())
    if "authorization" in metadata:
        authorization_header = metadata["authorization"]
        _, access_token = authorization_header.split("Bearer ")
        decoded_access_token = asyncio.get_event_loop().run_until_complete(
            decode_token(access_token)
        )
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
        return user
    else:
        user64 = metadata["x-delphai-user"]
        user = b64decode(user64)
        return json.loads(user)


def get_groups(context: ServicerContext) -> List[str]:
    """
    Gets groups of calling identity
    :param grpc.aio.ServicerContext context: context passed to grpc endpoints
    :return raw roles passed from keycloak.
      For example this can be ["/delphai/Development"]
    :rtype List[str]
    """

    assert isinstance(context, object)
    try:
        user = get_user(context)
    except KeyError:
        return []
    return user.get("groups") or []


def get_affiliation(
    context: ServicerContext,
) -> Tuple[Union[str, None], Union[str, None]]:
    """
    Gets organization and department of user
    :param grpc.aio.ServicerContext context: context passed to grpc endpoints
    :return organization and department as a tuple or None if not affiliated
    :rtype Union[Tuple[str, None], Tuple[str, None]]
    """

    raw_groups = get_groups(context)
    if len(raw_groups) == 0:
        return None, None
    else:
        group_hirarchy = raw_groups[0].split("/")[1:3]
        if len(group_hirarchy) == 1:
            return group_hirarchy.pop(), None
        elif len(group_hirarchy) == 2:
            return tuple(group_hirarchy)
        else:
            return None, None


def get_user_and_client_ids(context: ServicerContext) -> Tuple[str, str]:
    """
    Get user_id and client_id.
    :param grpc.aio.ServicerContext context: context passed to grpc endpoints
    :return user_id and client_id.
      More information: https://wiki.delphai.dev/wiki/Authorization
    :rtype: Tuple[str, str]
    """
    try:
        user = get_user(context)
        user_id = user.get("https://delphai.com/mongo_user_id")
        client_id = user.get("https://delphai.com/client_id")
    except Exception:
        return "", ""
    return user_id, client_id

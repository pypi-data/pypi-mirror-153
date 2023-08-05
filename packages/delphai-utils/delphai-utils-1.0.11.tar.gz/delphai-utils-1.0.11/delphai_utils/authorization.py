from typing import List, Union
from delphai_utils.users import get_user
from grpc import StatusCode
from grpc.aio import ServicerContext
import asyncio
from functools import wraps


def get_roles(provided_roles: Union[List[str], ServicerContext]):
    """
    Utility function to retrieve roles from grpc context.
    :param Union[List[str], grpc.aio.ServicerContext] provided_roles:
      a list of roles or the grpc context passed to class methods
    :return list of roles
    :rtype List[str]
    """

    assert isinstance(provided_roles, object) or type(provided_roles) == list
    if type(provided_roles) is not list:
        try:
            user = get_user(provided_roles)
            return user.get("roles") or []
        except KeyError:
            return []
    else:
        return provided_roles


def is_authorized(
    provided_roles: Union[List[str], ServicerContext],
    required_roles: List[str],
    decission_logic: str = "all",
    abort: bool = False,
):
    """
    Makes a decision if user is authorized based on intersection of roles.
    :param Union[List[str], grpc.aio.ServicerContext] provided_roles:
      a list of roles or the grpc context passed to class methods
    :param List[str] required_roles: roles the request must pass
    :param str decission_logic: one of 'all' or 'some'. Default: 'all'
    :param bool abort: if set to true grpc call will abort with PERMISSION_DENIED. Default: False
    :rtype: bool
    """

    assert len(required_roles) != 0
    assert type(required_roles) == list
    assert any([allowed == decission_logic for allowed in ["all", "some"]])
    resolved_roles = get_roles(provided_roles)

    required_roles = set(required_roles)  # in case same role is passed mulitple times
    role_intersection = required_roles.intersection(resolved_roles)
    all_intersects = len(role_intersection) == len(required_roles)
    some_intersects = len(role_intersection) > 0
    _is_authorized = (decission_logic == "all" and all_intersects) or (
        decission_logic == "some" and some_intersects
    )
    is_grpc_context = type(provided_roles) is not list
    if abort and not is_authorized and is_grpc_context:
        details = f"Provided roles {resolved_roles} don't intersect with required roles {required_roles}."
        provided_roles.abort(StatusCode.PERMISSION_DENIED, details)
    return _is_authorized


def authorize(required_roles: List[str], decission_logic: str = "all"):
    """
    Decorator for grpc endpoints to restrict role-based access.
    :param List[str] required_roles: list of strings which roles are required
    :param str decission_logic: one of 'all' or 'some'. Default: 'all'
    :return: wraped function
    :rtype: func
    """

    def wrap(func):
        if not asyncio.iscoroutinefunction(func):

            @wraps(func)
            def wrapped_func(self, request, context, *args, **kwargs):
                if is_authorized(context, required_roles, decission_logic):
                    return func(self, request, context, *args, **kwargs)
                else:
                    details = f"Given roles don't intersect with {required_roles} using decission logic '{decission_logic}'"
                    context.abort(StatusCode.PERMISSION_DENIED, details)

            return wrapped_func
        else:

            @wraps(func)
            async def wrapped_func(self, request, context, *args, **kwargs):
                if is_authorized(context, required_roles, decission_logic):
                    return await func(self, request, context, *args, **kwargs)
                else:
                    details = f"Given roles don't intersect with {required_roles} using decission logic '{decission_logic}'"
                    await context.abort(StatusCode.PERMISSION_DENIED, details)

            return wrapped_func

    return wrap

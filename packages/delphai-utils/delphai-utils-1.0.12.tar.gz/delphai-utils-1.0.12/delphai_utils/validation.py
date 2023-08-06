from delphai_utils.validator import validate as _validate, ValidationFailed
from grpc import StatusCode


async def validate(descriptor, value, context):
    try:
        validated = _validate(descriptor)(value)
        return
    except ValidationFailed as ex:
        args = list(ex.args)
        errors = list(map(lambda err: err.replace("p.", ""), args))
        await context.abort(StatusCode.INVALID_ARGUMENT, ", ".join(errors))

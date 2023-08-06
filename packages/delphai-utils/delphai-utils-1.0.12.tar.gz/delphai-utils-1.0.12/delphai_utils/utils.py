import os, signal, threading, sys
from delphai_utils.logging import logging
import asyncio
from functools import partial, wraps


# Disable
def block_print():
    sys.stdout = open(os.devnull, "w")


# Restore
def enable_print():
    sys.stdout = sys.__stdout__


def _signal_handler(sig, frame):
    logging.info("stopping server...")
    sys.exit(0)


def wait_for_exit():
    signal.signal(signal.SIGINT, _signal_handler)
    forever = threading.Event()
    forever.wait()


def async_wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)

    return run


def generate_default_message(message_descriptor, lvls: int = 10):
    """
    Returns descriptive template for message.
    """
    if lvls == 0:
        return "..."
    res = {}
    for fld in message_descriptor.fields:
        if fld.message_type:
            fld_content = generate_default_message(fld.message_type, lvls - 1)
        else:
            fld_content = fld.default_value
        if fld.default_value == []:
            if fld.message_type:
                fld_content = [
                    fld_content,
                ]
            elif fld.type == 9:  # string
                fld_content = [
                    "",
                ]
            elif fld.type == 2:  # float
                fld_content = [
                    0.0,
                ]
            elif fld.type == 8:  # boolean
                fld_content = [
                    False,
                ]
            elif fld.type in [3, 5]:  # int32, int64
                fld_content = [
                    0,
                ]
        res[fld.name] = fld_content
    return res

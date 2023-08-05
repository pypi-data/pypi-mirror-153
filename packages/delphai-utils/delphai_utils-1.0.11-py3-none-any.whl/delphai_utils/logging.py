from logging import error, warn, info, debug  # noqa: F401
import logging
import logging.config
from sys import exc_info
from traceback import format_tb
from deepmerge import always_merger
import coloredlogs
from delphai_utils.config import get_config

default_config = {
    "version": 1,
    "disable_existing_loggers": True,
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        }
    },
    "formatters": {
        "standard": {
            "format": "[%(asctime)s] [%(levelname)s] %(message)s",
            "datefmt": "%H:%M:%S",
        }
    },
    "loggers": {"": {"level": "INFO", "handlers": ["default"]}},
}


def _configure_logging():
    provided_config = {}
    try:
        provided_config = get_config("logging")
    except Exception:
        pass
    logging_config = always_merger.merge(default_config, provided_config)
    standard_format = logging_config["formatters"]["standard"]

    logging.config.dictConfig(logging_config)
    level = logging.getLevelName(logging.getLogger().getEffectiveLevel())
    coloredlogs.install(
        level=level, fmt=standard_format["format"], datefmt=standard_format["datefmt"]
    )


def error_with_traceback():
    """
    Writes to log an occured exception with a last line of traceback
    """
    einfo = exc_info()
    exc_class = einfo[0].__name__
    exc_descr = str(einfo[1])
    traceback = format_tb(einfo[2])
    traceback = "\n" + traceback[-1].strip() if traceback else ""
    logging.error(f"{exc_class}: {exc_descr}{traceback}")


_configure_logging()

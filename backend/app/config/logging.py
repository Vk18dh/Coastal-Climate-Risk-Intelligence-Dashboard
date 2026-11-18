"""Configure application-wide structured logging."""
import logging
import sys

from app.config.settings import settings

_NOISY_LOGGERS = [
    "uvicorn.access",
    "asyncio",
]


def configure_logging() -> None:
    """
    Set up the root logger with a consistent format and the log level
    specified in application settings.

    Called once at application startup in main.py, before any other
    module emits log output.
    """
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)-40s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers.clear()
    root_logger.addHandler(handler)

    # Suppress noisy third-party loggers that are not useful at INFO level
    for name in _NOISY_LOGGERS:
        logging.getLogger(name).setLevel(logging.WARNING)

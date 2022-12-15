# Custom Logger Using Loguru

import logging
import sys

from loguru import logger

from base.configs import settings


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: "CRITICAL",
        40: "ERROR",
        30: "WARNING",
        20: "INFO",
        10: "DEBUG",
        0: "NOTSET",
    }

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id="app")
        log.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def customize_logging():
    logger.remove()

    logger.add(
        sys.stdout,
        enqueue=True,
        backtrace=True,
        level="INFO",
        diagnose=settings.LOG_DIAGNOSE,
        format=settings.LOG_FORMAT,
    )

    # get INFO logs
    logger.add(
        settings.LOG_INFO_FILE,
        rotation=settings.LOG_ROTATION,
        retention=settings.LOG_RETENTION,
        enqueue=True,
        diagnose=settings.LOG_DIAGNOSE,
        backtrace=True,
        level="INFO",
        format=settings.LOG_FORMAT,
    )

    # get ERROR logs
    logger.add(
        settings.LOG_ERROR_FILE,
        rotation=settings.LOG_ROTATION,
        retention=settings.LOG_RETENTION,
        enqueue=True,
        diagnose=settings.LOG_DIAGNOSE,
        backtrace=True,
        level="ERROR",
        format=settings.LOG_FORMAT,
    )

    # get CUSTOM logs
    logger.add(
        settings.LOG_ERROR_FILE,
        rotation=settings.LOG_ROTATION,
        retention=settings.LOG_RETENTION,
        enqueue=True,
        diagnose=settings.LOG_DIAGNOSE,
        backtrace=True,
        level="DEBUG",
        format=settings.LOG_FORMAT,
        filter=lambda record: "custom" in record["extra"],
    )

    logging.basicConfig(handlers=[InterceptHandler()])
    logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
    for _log in ["uvicorn", "uvicorn.error", "fastapi"]:
        _logger = logging.getLogger(_log)
        _logger.handlers = [InterceptHandler()]

    return logger.bind(request_id=None, method=None)


logger = customize_logging()

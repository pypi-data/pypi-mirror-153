import logging

import colorlog

DEBUG1 = 9
DEBUG2 = 8
DEBUG3 = 7


def debugv(self, message, level, *args, **kwargs):
    if self.isEnabledFor(level):
        self._log(level, message, args, **kwargs)


def debug1(self, message, *args, **kwargs):
    debugv(self, message, logging.DEBUG1, *args, **kwargs)


def debug2(self, message, *args, **kwargs):
    debugv(self, message, logging.DEBUG2, *args, **kwargs)


def debug3(self, message, *args, **kwargs):
    debugv(self, message, logging.DEBUG3, *args, **kwargs)


def setup_logging():
    logging.DEBUG1 = DEBUG1
    logging.DEBUG2 = DEBUG2
    logging.DEBUG3 = DEBUG3
    logging.Logger.debug1 = debug1
    logging.Logger.debug2 = debug2
    logging.Logger.debug3 = debug3
    logging.addLevelName(logging.DEBUG1, "DEBUG1")
    logging.addLevelName(logging.DEBUG2, "DEBUG2")
    logging.addLevelName(logging.DEBUG3, "DEBUG3")


def configure_logging(level=logging.INFO):
    setup_logging()
    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            "%(log_color)s%(levelname)s%(reset)s | %(message)s",
            reset=True,
            log_colors={
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
                "DEBUG": "cyan",
                "DEBUG1": "thin_white",
                "DEBUG2": "thin_white",
                "DEBUG3": "thin_white",
            },
        )
    )
    logger = colorlog.getLogger(__name__)
    if not logger.handlers:
        logger.addHandler(handler)
    logger.setLevel(level)


def get_logger():
    setup_logging()
    logger = colorlog.getLogger(__name__)
    return logger

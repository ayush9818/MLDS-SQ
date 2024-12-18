import logging

logger = logging.getLogger(__name__)

DELAY = 1


def debug(msg="this is a debug message"):
    logger.debug(msg)


def info(msg="this is an info message"):
    logger.info(msg)


def warning(msg="this is a warning message"):
    logger.warning(msg)


def error(msg="this is an error message"):
    logger.error(msg)

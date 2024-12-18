import logging

# Logger configuration is left up to the executing script
logger = logging.getLogger(__name__)


def test_logging():
    logger.debug("Debuggggg")
    logger.info("FYI")
    logger.warning("Warning!")

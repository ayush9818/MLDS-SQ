import logging.config
import logging

logging.basicConfig(filename="logs/msia423.log", level=logging.DEBUG)
logger = logging.getLogger("msia423-demo")

logger.debug("Debuggggg")
logger.info("FYI")
logger.warning("Warning!")

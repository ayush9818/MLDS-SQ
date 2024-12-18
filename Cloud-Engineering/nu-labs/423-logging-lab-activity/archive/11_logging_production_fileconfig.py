import logging.config
import logging

logging_config = "config/logging_prod.conf"

logging.config.fileConfig(logging_config)
logger = logging.getLogger("msia423-demo")

logger.debug("Debuggggg")
logger.info("FYI")
logger.warning("Warning!")

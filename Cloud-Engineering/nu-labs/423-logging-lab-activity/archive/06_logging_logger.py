import logging

logging.basicConfig(
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S %p",
    level=logging.DEBUG,
)

# Will display 'msia423-logging-module' instead of 'root'
logger = logging.getLogger("msia423-demo")

class_name = "MSIA423"
description = "fun!"

logging.warning("%s is so %s", class_name, description)
logger.warning("%s is so %s", class_name, description)

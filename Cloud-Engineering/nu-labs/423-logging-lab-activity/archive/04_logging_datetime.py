import logging

logging.basicConfig(
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S %p",
    level=logging.DEBUG,
)

logging.debug("Debuggggg")
logging.info("FYI")
logging.warning("Warning!")

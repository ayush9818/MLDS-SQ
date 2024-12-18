import logging

from src.logmodule import test_logging

# Chaning level to "Warning"
logging.basicConfig(
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S %p",
    level=logging.WARNING,
)

test_logging()

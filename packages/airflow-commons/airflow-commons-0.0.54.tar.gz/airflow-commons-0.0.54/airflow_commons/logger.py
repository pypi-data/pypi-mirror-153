import logging
from time import gmtime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(filename)s | %(funcName)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logging.Formatter.converter = gmtime

LOGGER = logging.getLogger("Commons")


def get_logger(name: str):
    return logging.getLogger(name)

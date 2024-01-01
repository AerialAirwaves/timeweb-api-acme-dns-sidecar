import logging

logging_format = "%(asctime)s - %(levelname)s - %(module)s - %(funcName)s: %(message)s"


def setup_logging(logging_level: str = logging.INFO):
    logging.basicConfig(level=logging_level, format=logging_format)

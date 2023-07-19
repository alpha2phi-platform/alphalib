import logging


def create_logger():
    logger = logging.getLogger(__name__)
    logger.propagate = False
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - [ %(filename)s:%(lineno)s - %(funcName)s() - %(levelname)s ] %(message)s"
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


# Create the logger
logger = create_logger()

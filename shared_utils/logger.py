import logging


def get_logger():
    logger = logging.getLogger('MyLogger')
    logger.setLevel(logging.INFO)  # Set the logging level
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger

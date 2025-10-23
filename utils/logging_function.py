import logging

def setup_logger(logfile=None, loglevel=logging.INFO):
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(loglevel)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Create a stream handler to log to the console
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if logfile:
        # Create a file handler to log to a file
        file_handler = logging.FileHandler(logfile)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

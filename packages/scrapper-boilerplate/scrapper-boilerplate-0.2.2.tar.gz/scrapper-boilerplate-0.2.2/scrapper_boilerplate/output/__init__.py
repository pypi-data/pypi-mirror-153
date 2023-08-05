import logging


def log(message):
    """
    Logs a message to the console and file, if wish.
    """
    print(message)
    logging.info(message)
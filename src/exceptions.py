from src.config.logger import logger
import PySimpleGUI as sg


def log_error(message):
    """
    logs error and pops up warning, without raising an exception
    :param message: what it's about
    :return: nothing
    """
    logger.error(message)
    sg.popup(message)


class PTBDException(Exception):
    def __init__(self, message):
        super().__init__(message)
        logger.error(message)
        sg.popup(message)


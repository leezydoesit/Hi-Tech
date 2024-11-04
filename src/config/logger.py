import logging
import sys
import json
from src.config.config import Config


class FileFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'name': record.name,
            'message': record.getMessage(),
            'function_name': record.funcName,
            'module': record.module,
            'line_number': record.lineno,
            'process_id': record.process,
            'thread_id': record.thread
        }

        if record.levelno >= logging.ERROR:
            return json.dumps(log_data)


class ConsoleFormatter(logging.Formatter):
    def format(self, record):
        # define colors
        colors = {
            logging.ERROR: '\033[31m',
            logging.CRITICAL: '\033[31m',
            logging.WARNING: '\033[33m',
            logging.WARN: '\033[33m',
            logging.INFO: '\033[32m',
            logging.DEBUG: '\033[34m'
        }
        if record.levelno >= logging.ERROR:
            return f"{colors[record.levelno]}{'Please contact admin : '} {self.formatTime(record)} - {record.name} - {record.levelname} - {record.getMessage()}\033[0m"
        if record.levelno == logging.DEBUG:
            return f"{colors[record.levelno]}{self.formatTime(record)} - {record.name} - {record.levelname} - {record.getMessage()} - line num: {record.lineno} - function name: {record.funcName} - module: {record.module}\033[0m"
        else:
            return f"{colors[record.levelno]}{self.formatTime(record)} - {record.name} - {record.levelname} - {record.getMessage()}\033[0m"


class TBDLogger(logging.Logger):
    """
    An instance of this class is used for all logging in the application
    """

    def __init__(self, name):
        super().__init__(name)
        self.config = Config()
        self.logger = logging.getLogger(name)

        # set the overall minimum threshold for logging
        self.logger.setLevel(self.config.logging_min_log_level)

        # set the STDOUT logging
        self.console_formatter = ConsoleFormatter()
        self.console_handler = logging.StreamHandler(sys.stdout)
        self.console_handler.setLevel(self.config.logging_console_min_log_level)
        self.console_handler.setFormatter(self.console_formatter)
        self.addHandler(self.console_handler)

        # set the File logging
        file_formatter = FileFormatter()
        file_handler = logging.FileHandler(self.config.logging_log_file_path)
        file_handler.setLevel(self.config.logging_file_min_log_level)
        file_handler.setFormatter(file_formatter)
        self.addHandler(file_handler)


logger = TBDLogger(__name__)

# tests
if __name__ == '__main__':
    # Logger can be tested here, messages can be further formatted
    logger = TBDLogger(__name__)
    logger.info('Info message')
    logger.warning('Warning message')
    logger.error('Error message')
    logger.critical('Critical message')


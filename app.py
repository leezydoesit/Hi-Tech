from src.config.logger import logger
from src.controller import run
from multiprocessing import freeze_support


if __name__ == '__main__':
	freeze_support()
	logger.debug("app starts")
	run()
	logger.debug("app exits")
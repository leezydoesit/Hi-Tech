import time
from src.config.logger import logger
import random
from random import uniform


def slow_type(what, where):
    logger.debug(f"slow_type start")
    for c in what:
        time.sleep(uniform(0, 0.3))
        where.send_keys(c)


def wait_a_bit_sir():
    logger.debug(f"wait_a_bit_sir start")
    # generate a random delay between range in seconds
    delay = random.randint(2, 6)
    time.sleep(delay)  # pause execution for the specified number of seconds


if __name__ == '__main__':
    start_time = time.time()
    wait_a_bit_sir()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nElapsed time: {elapsed_time} seconds")
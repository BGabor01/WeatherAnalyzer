import functools
import time
import logging

from exceptions import MaxRetryError

logger = logging.getLogger("data_collector")


def retry(max_retries: int = 3, delay: int = 3, exceptions: tuple = (Exception,)):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < max_retries:
                try:
                    return function(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    logger.warning(e)
                    time.sleep(delay)
            raise MaxRetryError(
                f"Function {function.__name__} failed after {max_retries} retries"
            )

        return wrapper

    return decorator

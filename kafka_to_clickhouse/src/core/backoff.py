import time
import logging
from functools import wraps


logger = logging.getLogger(__name__)


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    """
    Функция для повторного выполнения функции через некоторое время,
    если возникла ошибка. Использует наивный экспоненциальный рост
    времени повтора (factor) до граничного времени ожидания
    (border_sleep_time)

    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time

    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            attempt = 1
            while True:
                t = 0
                try:
                    if t < border_sleep_time:
                        t = start_sleep_time * factor**attempt
                    if t >= border_sleep_time:
                        t = border_sleep_time
                    time.sleep(t)
                    attempt += 1
                    res = func(*args, **kwargs)
                except Exception as ex:
                    error_msg = f"Exception {func.__name__}: {ex}"
                    logger.error(error_msg)
                    logger.warning(f"Wait {t} seconds and try again...")
                else:
                    return res

        return inner

    return func_wrapper

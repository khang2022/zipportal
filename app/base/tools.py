import time
import tracemalloc

from base.log import logger


def time_benchmark(func):
    """
    Logging how much time a function takes
    """

    def profile(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        logger.info(f"Function {func.__name__} takes {end - start}s")
        return res

    profile.__name__ = func.__name__
    return profile


def memory_benchmark(func):
    """
    Logging how much memory a function takes
    """

    def profile(*args, **kwargs):
        tracemalloc.start()
        res = func(*args, **kwargs)
        cur, peak = tracemalloc.get_traced_memory()
        logger.info(
            f"Function {func.__name__} takes {cur} byte now in memory "
            f"and peak size in memory is {peak} byte"
        )
        tracemalloc.stop()
        return res

    profile.__name__ = func.__name__
    return profile

from functools import wraps
import time

from logs.logger_config import setup_logger


logger = setup_logger()



def timing_performance(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        logger.info(f"Début {func.__name__}")
        start = time.perf_counter()
        res = func(*args,**kwargs)
        logger.info(f"Fin {func.__name__} {time.perf_counter()-start:.3f}s")
        return res
    return wrapper
from django.utils.decorators import method_decorator
from functools import wraps
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def logger_decorator(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            result = str(e)
        finally:
            logger.debug(f"{func.__name__} called with args: {args} and kwargs: {kwargs} resulting: {result}")
        return result
    return inner

class Test:
    @method_decorator(logger_decorator)
    def hello_world(self):
        return "hello"

Test().hello_world()
print("Script completed successfully, no errors.")

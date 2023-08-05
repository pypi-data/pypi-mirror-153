"""
LogDecorator for logging errors of try-except handling.
"""
from functools import wraps

from log_handler import Logger
from options import Options


class LogDecorator:
    """
    Class decorator for logs.
    """
    def __init__(self, message):
        self.logger = Logger()
        self.message = message

    def __call__(self, fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            try:
                if Options.log_level in ('INFO', 'DEBUG'):
                    self.logger.log(fn.__name__, self.message)
                return fn(*args, **kwargs)
            except Exception as ex:
                self.logger.log(fn.__name__, f'ERROR - {ex}')
                raise ex

        return decorated


#
# def exception_handler(log: Logger):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):  # type: ignore
#             try:
#                 response = func(*args, **kwargs)
#             except es_exception.SerializationError:
#                 log.critical("serialization error!")
#                 raise
#             except es_exception.ConnectionError:
#                 log.critical("connection error!", extra={"update_func_name": func.__name__})
#                 raise
#             except es_exception.RequestError:
#                 log.critical("request error!")
#                 raise
#             except Exception as err:
#                 log.critical(f"uncaught error! :{err}")
#                 raise
#
#             return response
#         return wrapper
#     return decorator


# def elasticsearch_async_exception_handler(func):
#     @wraps(func)
#     async def inner_func(*args, **kwargs):
#         try:
#             response = await func(*args, **kwargs)
#         except es_exception.SerializationError:
#             logging.critical("serialization error!")
#             raise
#         except es_exception.ConnectionError:
#             logging.critical("connection error!")
#             raise
#         except es_exception.RequestError:
#             logging.critical("request error!")
#             raise
#         except Exception as err:
#             logging.critical(f"uncaught error! :{err}")
#             raise
#         return response
#     return inner_func
#
#
#
# import asyncio
#
#
# loop = asyncio.get_event_loop()
# coroutine = custom_search(es, "index", {"query": {"match_all": {}}})
# loop.run_until_complete(coroutine)


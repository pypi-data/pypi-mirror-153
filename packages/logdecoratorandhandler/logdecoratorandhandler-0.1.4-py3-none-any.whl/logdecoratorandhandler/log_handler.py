"""
LogHandler for chaining log levels.
"""
import json
import uuid
from logging import basicConfig, INFO, getLogger
from logging import getLogRecordFactory, setLogRecordFactory

# unique export id
from .options import Options

EXPORT_ID = uuid.uuid4()


basicConfig(format=json.dumps({'created_at': '%(asctime)s',
                               'thread_id': '%(thread)s',
                               'logger_name': '%(name)s',
                               'log_levelname': '%(levelname)s',
                               'export_id': '%(export_id)s',
                               'log_message': '%(message)s'}
                              ),
            level=INFO,
            filename=Options.file_name,
            )
old_factory = getLogRecordFactory()


def record_factory(*args, **kwargs):
    """
    Add additional features to logs.
    """
    record = old_factory(*args, **kwargs)
    record.export_id = str(EXPORT_ID)
    return record


setLogRecordFactory(record_factory)


class IHandler:
    """
    Parent handler for different log levels.
    """
    def __init__(self):
        self.logger = getLogger(Options.logger_name)

    def handle(self, function_name, message):
        pass


class InfoHandler(IHandler):
    """
    Logs info.
    """
    def __init__(self, next_):
        super().__init__()
        self.next = next_

    def handle(self, function_name: str, message: str) -> None:
        if message.startswith('INFO'):
            self.logger.info(f'{message} - function: {function_name}')
        else:
            self.next.handle(function_name, message)


class ErrorHandler(IHandler):
    """
    Logs error.
    """
    def __init__(self, next_):
        super().__init__()
        self.next = next_

    def handle(self, function_name: str, message: str) -> None:
        """
        Add here what should happen if error - e.g. send e-mail.
        """
        if message.startswith('ERROR'):
            self.logger.error(f'{message} - function: {function_name}')
        else:
            self.next.handle(function_name, message)


class DebugHandler(IHandler):
    def __init__(self, next_):
        super().__init__()
        self.next = next_

    def handle(self, function_name: str, message: str) -> None:
        if message.startswith('DEBUG'):
            self.logger.debug(f'{message} - function: {function_name}')
        else:
            self.next.handle(function_name, message)


class DefaultHandler(IHandler):
    """
    Default logger gives warning for unsupported message type.
    """
    def handle(self, function_name: str, message: str) -> None:
        self.logger.warning(f'WARNING - unsupported message type - function: {function_name}, ')


class Logger:
    """
    Chain of responsibility.
    """
    def __init__(self):
        default_handler = DefaultHandler()
        error_handler = ErrorHandler(default_handler)
        info_handler = InfoHandler(error_handler)
        debug_handler = DebugHandler(info_handler)
        self.handler = debug_handler

    def log(self, function_name: str, message: str) -> None:
        """
        Logs level depending on message.
        """
        self.handler.handle(function_name, message)

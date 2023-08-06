"""
Options for log level.
"""
from dataclasses import dataclass, field


@dataclass
class Options:
    """
    Add additional options - e.g. mail if error...
    """
    log_level: str = field(default='ERROR')
    logger_name: str = field(default='log_decorator')
    file_name: str = field(default='logging.log')

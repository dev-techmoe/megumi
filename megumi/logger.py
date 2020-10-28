import logging
from colorlog import ColoredFormatter, StreamHandler
from typing import Union

def update_root_logger(log_level: Union[str, int], stdout_enable_ansi: bool=True):
    format_text = '[%(levelname)-7s] %(message)s'

    root_logger = logging.getLogger('megumi')
    root_logger.setLevel(log_level)
    # stdout handler
    stdout_handler = StreamHandler()
    if stdout_enable_ansi:
        stdout_handler.setFormatter(ColoredFormatter('%(log_color)s' + format_text))
    else:
        stdout_handler.setFormatter(logging.Formatter(format_text))
    root_logger.addHandler(stdout_handler)

import click
from .daemon import daemon
from .job import job
from ..config import config
import logging
import os
from ..logger import update_root_logger
import logging
from colorlog import ColoredFormatter, StreamHandler

@click.group()
@click.option(
    '-c',
    '--config-path',
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    help='Path for config file.'
)
@click.option(
    '--log-level',
    type=click.Choice(['ERROR', 'INFO', 'DEBUG'], case_sensitive=False),
    help='Logging level',
    default='INFO'
)
@click.option(
    '--no-ansi',
    default=False,
    is_flag=True,
    help='Disable ANSI color output (You can also set this by setting the environment variable NO_COLOR to TRUE)'
)
def cli(config_path=None, log_level=None, no_ansi=False):
    # update logger level
    if not log_level == None:
        config.logging.set('level', log_level)
    # init logger
    format_text = '[%(levelname)-7s] %(message)s'
    root_logger = logging.getLogger('megumi')
    root_logger.setLevel(log_level)
    # stdout handler
    stdout_handler = logging.StreamHandler()
    if config.logging.no_ansi or os.getenv('NO_COLOR') == '1': 
        stdout_handler.setFormatter(ColoredFormatter('%(log_color)s' + format_text))
    else:
        stdout_handler.setFormatter(logging.Formatter(format_text))
    root_logger.addHandler(stdout_handler)

    # read config
    logger = logging.getLogger('megumi.cli')
    if config_path:
        logger.debug('Load config from %s', config_path)
        try:
            config.load_from_file(config_path, 'toml')
            # XXX: dont make logging config from config file overwrite them from cli
            root_logger.setLevel(log_level)
        except Exception as err:
            logger.error('Failed to read config. %s', repr(err))
            exit(-1)

cli.add_command(daemon)
cli.add_command(job)
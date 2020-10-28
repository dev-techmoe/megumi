from .abc import DownloaderConnector
from .aria2c import Aria2cConnector

connectors = {
    'aria2': Aria2cConnector
}

__all__ = ['DownloaderConnector', 'Aria2cConnector', 'connectors']
from abc import ABCMeta, abstractmethod

class DownloaderConnector(metaclass=ABCMeta):

    @abstractmethod
    async def download_by_url(self, url: str):
        pass
    
    @abstractmethod
    async def download_by_magnet_link(self, url: str):
        pass

    @abstractmethod
    async def download_by_torrent(self, torrent_binary: str):
        pass
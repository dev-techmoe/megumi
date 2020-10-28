from .downloader_connector.abc import DownloaderConnector
from .db import DAO
from .rss import rss
from logging import getLogger
import asyncio
import aiohttp

class Scheduler:
    def __init__(self, download_connector: DownloaderConnector, dao: DAO):
        self.dao = dao
        self.download_connector = download_connector
        self.logger = getLogger('megumi.scheduler')
    
    def run_loop(self):
        asyncio.get_event_loop().run_until_complete(self.__async__run_loop())

    async def __async__run_loop(self):
        while True:
            try:
                async for rss_info, latest_item in rss.get_updates():
                    bt_src = latest_item['enclosure_url']
                    if bt_src == None:
                        self.logger.warning(f'Failed to find enclosure url in RSS item. url={latest_item["link"]}')

                    try:
                            # XXX
                            self.logger.info(f'Push task to downloader. task_id={rss_info["__id"]} link={bt_src}')
                            await self.push_task(bt_src)
                            # TODO: run hook here
                            self.dao.update_task_status(rss_info['__id'], latest_item['date'], bt_src, True)
                    except:
                        self.logger.exception('Failed to send task to downloader.')
                        self.dao.update_task_status(rss_info['__id'], latest_item['date'], bt_src, False)
            except:
                self.logger.exception('Failed to get latest rss updates.')

            await asyncio.sleep(10)
    
    async def push_task(self, link: str):
        self.logger.debug(f'Start send task to downloader. url="{link}"')
        if link.startswith('magnet'):
            self.download_connector.download_by_magnet_link(link)
        elif link.startswith('http'):
            async with aiohttp.ClientSession(trust_env=True) as sess:
                self.logger.debug(f'Start download torrent file.')
                resp = await sess.get(link)
                binary = await resp.read()

            await self.download_connector.download_by_torrent(binary)
        else:
            self.logger.warning(f'Unsupported link type: {link}')
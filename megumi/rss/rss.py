import asyncio
import aiohttp
import async_timeout
import logging
from xml.etree.ElementTree import fromstring
from email.utils import parsedate_to_datetime
from ..db import DAO

logger = logging.getLogger('megumi.rss_checker')

async def get_rss_content(url: str) -> list:
    result = []

    async with aiohttp.ClientSession(trust_env=True) as sess:
        logger.debug(f'Start fetching {url}')
        resp = await sess.get(url)
        doc = fromstring(await resp.text())

        desc = doc.find('channel/description')
        if desc:
            desc = desc.text

        for i in doc.iterfind('channel/item'):
            item = {}
            # RFC822
            item['date'] = parsedate_to_datetime(i.findtext('pubDate')).timestamp()
            item['title'] = i.findtext('title')
            item['description'] = i.findtext('description')
            item['link'] = i.findtext('link')
            item['enclosure_url'] = i.find('enclosure').attrib['url']

            result.append(item)
    
    return result

async def get_updates():
    dao = DAO.get_instance()
    all_rsses = dao.get_all_job()
    logger.info('Start checking new item of all RSS')
    for r in all_rsses:
        try:
            logger.debug(f'Fetching RSS url: {r["url"]}')
            rss_data = await get_rss_content(r['url'])
        except:
            logger.exception(f'Failed to get RSS data. url={r["url"]}')
            continue

        if int(rss_data[0]['date']) > r['lastPubTime']:
            data = filter(lambda d: d['date'] > r['lastPubTime'], rss_data)
            for i in data:
                yield r, i
        else:
            logger.info('No updates found.')
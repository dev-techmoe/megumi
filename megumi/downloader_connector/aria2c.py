from .abc import DownloaderConnector
from typing import List, Dict
from aiohttp import ClientSession
import uuid
import json
import base64
import logging
import asyncio

class RPCError(Exception):
    def __init__(self, payload):
        self.payload = payload
        self.message = payload['message']

class Aria2cConnector(DownloaderConnector):
    def __init__(self, connector_info: Dict=None):
        """
        connector_info example
        {
            'address': 'http://localhost:6800',
            'secret': 'sasasa'
        }
        """
        self.logger = logging.getLogger('megumi.connector.aria2c')
        self.connector_info = connector_info
        self.rpc_address = connector_info['address'] + '/jsonrpc'
        self.rpc_secret = connector_info.secret
        
        self.aio_session = ClientSession()
    
    async def download_by_url(self, url: str):
        resp = await self.call_aria2c_rpc('aria2.addUri', [ url ])
        return resp['result']

    async def download_by_magnet_link(self, url: str):
        return await self.download_by_url(url)

    async def download_by_torrent(self, torrent_binary: any):
        resp = await self.call_aria2c_rpc('aria2.addTorrent', base64.b64encode(torrent_binary).decode('utf-8'))
        return resp['result']
    
    async def call_aria2c_rpc(self, method: str, params: any):
        resp = await self.aio_session.post(self.rpc_address, data=json.dumps({
            'jsonrpc': '2.0',
            'id': str(uuid.uuid4()),
            'method': method,
            'params': [ f'token:{self.rpc_secret}', params ]
        }))
        resp_json = await resp.json()
        self.logger.debug('Aria2c resp: %s', resp_json)
        if 'error' in resp_json.keys():
            raise RPCError(resp_json.get('error'))
        
        return resp_json
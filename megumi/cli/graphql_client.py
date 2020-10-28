import aiohttp
import asyncio
from typing import List, Dict
from megumi.config import config
from typing import Tuple
import toml
import json
import os

address = None

def get_info_file_path() -> 'str':
    return os.path.join(
        config.runtime.data_path,
        'conn_info.toml'
    )

def write_api_conn_info(auth_token, port):
    
    with open(get_info_file_path(), 'w') as f:
        f.write('# DO NOT MODIFY IT MANUALLY UNLESS YOU KNOW WHAT YOU ARE DOING\n\n')
        f.write(toml.dumps({
            'auth_token': auth_token,
            'port': port
        }))

# (api_address, api_secret)
conn_info_ext = (None, None)

def read_api_conn_info() -> Tuple[str, str]:
    if conn_info_ext[0] != None:
        return conn_info_ext

    conn_info = None
    try:
        conn_info = config['api']
    except KeyError:
        try:
            with open(get_info_file_path()) as f:
                conn_info = toml.load(f)
        except Exception as err:
            raise Exception('Failed to read connection info automatically, please specific it in argument list. %s', str(err))

    address = f'http://localhost:{conn_info["port"]}'
    return address, conn_info['auth_token']


class GraphqlExecutorException(Exception):
    def __init__(self, payload: List[Dict]):
        self.payload = payload
        self.message = payload[0]['message']

def run_query(query_string: str, params={}, address=None, token=None):
    if not address:
        address, token = read_api_conn_info()
    
    address += '/graphql'

    # TODO: add api token in query
    async def async_run_query():
        async with aiohttp.ClientSession() as sess:
            async with sess.post(
                address,
                data={
                    'query': query_string,
                    'variables': json.dumps(params)
                }
            ) as resp:
                data: dict = await resp.json()
                if 'errors' in data.keys():
                    # XXX
                    raise Exception(data['errors'])
                return data['data']

    return asyncio.run(async_run_query())
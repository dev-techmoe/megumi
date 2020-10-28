import pytest
from aiohttp import web
import json
from megumi.cli import graphql_client
import asyncio
import threading
from functools import partial
from pytest_aiohttp import aiohttp_server
from aiohttp import test_utils
from .utils.mock_server import get_mock_server

import toml

router = web.RouteTableDef()

@router.post('/graphql')
def graphql(request: web.Request):
    return web.json_response({
        'data': {
            'foo': 'bar'
        }
    })

test_server = get_mock_server(router)

def test_client(test_server):
    query = """
    query {
        foo {
            id
        }
    }
    """
    resp = graphql_client.run_query(
        address=f'http://localhost:{test_server["port"]}',
        query_string=query,
        params={
            'id': '123'
        },
        token='token'
    )

    assert resp['foo'] == 'bar'

def test_conn_info_rw(tmp_path):
    # graphql_client.INFO_FILE_PATH = str(tmp_path) + '/test.toml'
    conf_path = str(tmp_path) + '/test.toml'
    graphql_client.get_info_file_path = lambda : str(tmp_path) + '/test.toml'
    
    graphql_client.write_api_conn_info('token', 123)
    with open(conf_path) as f:
        conf = toml.load(f)
        assert conf['auth_token'] == 'token'
        assert conf['port'] == 123
    
    from megumi.config import config
    # config.load_config('./tests/assests/config_test_api_key.toml')
    config.load_from_file('./tests/assests/config_test_api_key.toml', 'toml')
    graphql_client.config = config
    address, secret = graphql_client.read_api_conn_info()
    assert address == 'http://localhost:123'
    assert secret == 'mytoken123'

    graphql_client.conn_info_ext = ('http://localhost:1234', '1234')
    address, token = graphql_client.read_api_conn_info()
    assert address == 'http://localhost:1234'
    assert token == '1234'
from megumi.downloader_connector.aria2c import Aria2cConnector, RPCError
import asyncio
from .utils.mock_server import get_mock_server
from aiohttp.web import RouteTableDef, json_response
from catconfig import CatConfig

router = RouteTableDef()

@router.post('/jsonrpc')
def jsonrpc(Req):
    return json_response({
        "id":"qwer",
        "jsonrpc":"2.0",
        "result":"2089b05ecca3d829"
    })

mock_server = get_mock_server(router)

async def test_aria2c_rpc(mock_server):
    port = mock_server['port']

    client = Aria2cConnector(CatConfig(data={
        'address': f'http://localhost:{port}',
        'secret': '1234'
    }))
    resp = await client.download_by_url('https://example.com')
    assert resp != None
    resp = await client.download_by_torrent(
        open('./tests/assests/ubuntu_iso_just_for_test.torrent', 'rb').read()
        )
    assert resp != None

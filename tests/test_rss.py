from megumi.db import DAO, get_db
from megumi.rss import rss
import unqlite
import asyncio
import os
from datetime import datetime
from aiohttp.web import RouteTableDef, Response
from .utils.mock_server import get_mock_server

router = RouteTableDef()

@router.get('/')
def rsssrv(req):
    with open('./tests/assests/test.xml') as f:
        txt = f.read()
        return Response(
            text=txt,
            content_type='application/xml',
            charset='utf-8'
        )

test_server = get_mock_server(router)

async def test_rss(test_server):
    db = get_db(mem_db=True)
    dao = DAO.get_instance()
    db.collection('jobs').store([{
        'lastPubTime': datetime.now().timestamp()-1000,
        'url': f'http://localhost:{test_server["port"]}'
    }])
    r = [i async for i in rss.get_updates()]
    
    assert r != None

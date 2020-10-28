from aiohttp import web
from aiohttp.web import Response
from logging import getLogger
import asyncio
from aiohttp_graphql import GraphQLView
from .graphql import root_schema as schema
from megumi.config import config

logger = getLogger('megumi.http')

app = web.Application(logger=logger)
routes = web.RouteTableDef()

temp_web_index = """
<html>
<head>
    <meta name="robots" content="noindex, nofollow">
</head>

<body>
    <p>WebUI WIP.</p>
    <p><a href="/graphql">GraphiQL Interface<a></p>
</body>
</html>
"""

@routes.get('/')
async def index(req):
    logger.debug('index be visited but nothing can be show now')
    return Response(body=temp_web_index, content_type='text/html')

async def async_launch_web():
    app.add_routes(routes)
    logger.debug(f'Launch web interface on {config.api.host}:{config.api.port}')
    GraphQLView.attach(app, schema=schema, graphiql=True)
    # await web._run_app(app, port=config['api']['port'])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '127.0.0.1', config.api.port)
    await site.start()

def launch_web():
    loop = asyncio.get_event_loop()
    loop.create_task(async_launch_web())

if __name__ == '__main__':
    from .. import logger as l
    from ..db import DAO
    DAO.get_instance()
    asyncio.run(async_launch_web())
import pytest
from aiohttp.web import RouteTableDef
from aiohttp import web
from aiohttp import test_utils
import asyncio
import threading

def get_mock_server(router: 'RouteTableDef'):

    @pytest.fixture()
    def test_server():
        app = web.Application()
        
        app.add_routes(router)

        port = test_utils.unused_port()
        print(f'listen on {port}')

        def run_server(loop: asyncio.AbstractEventLoop):
            # https://stackoverflow.com/questions/51610074/how-to-run-an-aiohttp-server-in-a-thread
            runner = web.AppRunner(app)
            loop.run_until_complete(runner.setup())
            site = web.TCPSite(runner, '127.0.0.1', port)
            loop.run_until_complete(site.start())
            loop.run_forever()

        loop = asyncio.new_event_loop()
        srv_thread = threading.Thread(target=run_server, args=(loop,))
        
        srv_thread.start()
        
        yield {'port': port}

        # https://stackoverflow.com/questions/46093238/python-asyncio-event-loop-does-not-seem-to-stop-when-stop-method-is-called
        loop.call_soon_threadsafe(loop.stop)
    
    return test_server
import click
from ..config import config
from ..version import VERSION
from ..db import get_db, DAO
from ..downloader_connector import connectors
from ..scheduler import Scheduler
from ..http_api.server import launch_web
from . import graphql_client
import asyncio
import os

@click.command()
def daemon():
    click.echo(click.style(f"\nMegumi - schedule downloading manager", fg="bright_white"))
    click.echo(click.style(f"Github: https://github.com/dev-techmoe/megumi", fg="bright_white"))
    click.echo(click.style(f"Version: {VERSION}\n", fg="bright_white"))

    # create runtime directory if not exists
    runtime_dir_path = config.runtime.data_path
    if not os.path.exists(runtime_dir_path):
        try:
            os.makedirs(runtime_dir_path)
        except Exception as err:
            click.echo(click.style(f'Failed to create runtime directory. {repr(err)}', fg="bright_red"))
            exit(-1)
    
    # init database
    get_db(os.path.join(runtime_dir_path, 'db'))

    # init dao
    dao = DAO.get_instance()

    # launch http server
    launch_web()

    # write conn info
    try:
        graphql_client.write_api_conn_info(config.api.auth_token, config.api.port)
    except KeyError:
        pass

    # init downloader connector
    downloader_type = config.downloader.type
    connector_class = connectors.get(downloader_type)
    connector = connector_class(config.downloader[downloader_type])

    # init scheduler
    scheduler = Scheduler(connector, dao)

    # run scheduler
    scheduler.run_loop()

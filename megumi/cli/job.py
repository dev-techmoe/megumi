import click
from ..db import DAO
from pprint import pprint
from . import graphql_client
from .graphql_client import run_query
# TODO: update config by request RESTful API

error = lambda msg: click.echo(click.style(msg, fg="bright_red"))
ok = lambda msg: click.echo(click.style(msg, fg="bright_white"))

@click.group()
@click.option('--api-address', type=click.STRING, default=None)
@click.option('--api-secret', type=click.STRING, default=None)
def job(api_address, api_secret):
    if api_address:
        graphql_client.conn_info_ext = (api_address, api_secret)

@job.command()
@click.argument('name', type=click.STRING)
@click.argument('url', type=click.STRING)
@click.option(
    '-s',
    '--save-path',
    help='Path for saving downloaded file.',
    default=None
)
def add(name: str, url: str, save_path: str):
    try:
        resp = run_query('''
        mutation($name: String, $url: String!, $enable: Boolean, $savePath: String) {
            createJob(data: {
                name: $name,
                url: $url,
                enable: $enable,
                savePath: $savePath
            }) {
                ok
                id
            }
        }
        ''', params={
            'name': name,
            'url': url,
            'savePath': save_path
        })
        ok(f'Job add successful, id={resp["createJob"]["id"]}')
    except Exception as err:
        error(f'Failed to add job. {repr(err)}')

@job.command()
def list():
    try:
        resp = run_query('''
        query {
            job {
                id
                name
                description
                url
                lastPubTime
                addAt
                enable
            }
        }
        ''')
        pprint(resp)
    except Exception as err:
        error(f'Failed to get job list. {err}')

@job.command()
@click.argument('job_id', type=int)
def delete(job_id):
    try:
        resp = run_query('''
        mutation($id: Int!) {
            deleteJob(id: $id) {
                ok
                id
            }
        }
        ''', params={ 'id': job_id })
        ok(f'Job delete successful. id={resp["deleteJob"]["id"]}')
    except Exception as err:
        error(f'Failed to delete job. {repr(err)}')

@job.command()
def history():
    dao = DAO.get_instance()
    pprint(dao.get_all_push_history())
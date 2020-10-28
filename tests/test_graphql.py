from megumi.http_api.graphql import root_schema
from megumi.db import get_db, clean_db, DAO
from megumi.db.db import db as db_instance
import pytest

@pytest.fixture(autouse=True)
def init_db():

    clean_db()
    db = get_db(mem_db=True)
    DAO._DAO__instance = None
    
    db.collection('jobs').store([{
        'name': 'test',
        'url': 'http://example.com/rss'
    }])

def test_job_list():
    data = root_schema.execute("""
    query {
        job {
            id
            name
            url
            savePath
        }
    }
    """)
    
    assert data.data['job'][0]['name'] == 'test'

def test_job_delete():
    data = root_schema.execute("""
    mutation {
        deleteJob(id: 0) {
            id
            ok
        }
    }
    """)

    assert data.data['deleteJob']['ok'] == True

def test_job_create():
    data = root_schema.execute('''
    mutation {
        createJob(data: {
            name: "auto_test",
            url: "test"
            enable: false
        }) {
            ok
            id
        }
    }
    ''')

    assert data.data['createJob']['ok'] == True
    assert get_db().collection('jobs') \
                .filter(lambda x: x['name'] == 'auto_test') != None

def test_job_update():
    data = root_schema.execute('''
    mutation {
        updateJob(data: {
            name: "new_name",
            url: "http://example.com/new_rss",
            enable: true
        }, id: 0) {
            ok
            id
        }
    }
    ''')
    
    assert data.data['updateJob']['ok'] == True

    db_data = get_db().collection('jobs') \
                    .fetch(0)
    assert db_data['enable'] == True
    
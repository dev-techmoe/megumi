from megumi.task import manager
from dataclasses import asdict
from megumi.db import get_db, clean_db, DAO
import pytest

@pytest.fixture
def db():
    clean_db()
    db = get_db(mem_db=True)
    DAO._DAO__instance = None
    db.collection('tasks').create()
    data = [asdict(manager.Task(
        status=1,
        url='http://example.com',
        downloaderTaskID=1
    ))]
    db.collection('tasks').store(data)
    yield db

def test_task_create(db):
    t = manager.TaskManager()
    t.create_task('http://newexample.com', job_id=123)

    a = db.collection('tasks').all()
    assert a[1]['url'] == 'http://newexample.com'
    assert a[1]['jobID'] == 123

def test_task_get(db):
    t = manager.TaskManager()
    task = t.get_task(0)

    assert task.id == 0
    assert task.url == 'http://example.com'

    tasks = t.get_all_task()
    assert tasks[0].id == 0

def test_task_update(db):
    t = manager.TaskManager()
    t.update_task(0, manager.Task(
        status=3
    ))

    tasks = t.get_all_task()
    assert tasks[0].status == 3
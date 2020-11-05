from megumi.db import get_database
from megumi.downloader_connector.abc import DownloaderConnector
from enum import Enum
from dataclasses import dataclass, asdict
from typing import List
from megumi.utils import get_utc_timestamp

class TaskStatus(Enum):
    CANCALED = 0
    PENDING = 1
    DOWNLOADING = 2
    FINISHED = 3
    ERROR = 4

@dataclass(init=False)
class Task:

    def __init__(self, *args: list, **kwargs: dict):
        if '__id' in kwargs:
            kwargs['id'] = kwargs['__id']
            del kwargs['__id']
        for (k, v) in kwargs.items():
            setattr(self, k, v)

    id: int = None
    status: int = 1
    jobID: int = None
    url: str = ''
    downloaderTaskID: str = ''
    downloaderStatus: int = 0
    downloaderLatestError: str = ''
    addAt: int = 0
    lastUpdateAt: int = 0

class TaskManager:

    def __init__(self):
        pass

    def create_task(self, url: str, run_immediately: bool = True, job_id: int = -1) -> int:
        utcts = get_utc_timestamp()
        task = Task(
            status=TaskStatus.PENDING.value,
            jobID=job_id,
            url=url,
            addAt=utcts,
            lastUpdateAt=utcts
        )
        with get_database('tasks') as (_, coll):
            coll.store([asdict(task)])

    def get_task(self, task_id: int) -> Task:
        with get_database('tasks') as (_, coll):
            data = coll.filter(lambda x: x['__id'] == task_id)
            if len(data) == 0:
                return None
            return Task(**data[0])
    
    def get_all_task(self) -> List[Task]:
        with get_database('tasks') as (_, coll):
            data = coll.all()
            return [Task(**d) for d in data]
    
    def update_task(self, task_id, data: Task):
        with get_database('tasks') as (_, coll):
            data.lastUpdateAt = get_utc_timestamp()
            coll.update(task_id, asdict(data))
    
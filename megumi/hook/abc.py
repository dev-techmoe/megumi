from abc import ABCMeta, abstractmethod
from enum import Enum

class HookType(Enum):
    JOB_ADD = 0
    JOB_REMOVE = 3
    TASK_BEFORE_PUSH = 1
    TASK_AFTER_PUSH = 2
    DOWNLOAD_COMPLETED = 4
    DOWNLOAD_FAILED = 5

class Hook(metaclass=ABCMeta):
    @abstractmethod
    async def execute(self, rss_info, latest_item_info):
        pass
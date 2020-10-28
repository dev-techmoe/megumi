from megumi import db
from typing import List, Dict
from datetime import datetime
import unqlite

class DAO:
    __instance = None

    def __init__(self, db: unqlite.UnQLite):
        super().__init__()
        self.db = db
    
    @classmethod
    def get_instance(cls) -> 'DAO':
        if cls.__instance == None:
            db_instance = db.get_db()
            cls.__instance = DAO(db_instance)

        return cls.__instance

    def get_all_job(self) -> List[Dict]:
        return self.db.collection('jobs').all()

    def add_job(self, info: Dict):
        info.update({
            'lastPubTime': datetime.now().timestamp(),
            'addAt': datetime.now().timestamp(),
            'enable': True
        })
        id = self.db.collection('jobs').store([info], return_id=True)
        self.db.commit()
        return id

    def update_job(self, id: int, data: Dict):
        result = self.db.collection('jobs').update(id, data)
        self.db.commit()
        return result

    def delete_job(self, id: int):
        result = self.db.collection('jobs').delete(id)
        self.db.commit()
        return result

    def get_job_by_id(self, id):
        return self.db.collection('jobs').fetch(id)

    # push history

    def get_all_push_history(self) -> List[Dict]:
        return self.db.collection('task_history').all()

    def get_push_history_by_id(self, source_id: int) -> List[Dict]:
        return self.db.collection('task_history') \
                    .filter(lambda d: d['sourceID'] == source_id)

    def add_push_history(self, data: Dict):
        self.db.collection('task_history').store([data])
        self.db.commit()

    def update_push_history(self, id: int, data: Dict):
        self.db.collection('task_history').update(id, data)
        self.db.commit()


    def update_task_status(self, source_id: int, last_pub_time: int, target_link: str, success=True):
        with self.db.transaction():
            if success:
                coll_jobs = self.db.collection('jobs')
                task_info = coll_jobs.fetch(source_id)
                task_info.update({ 'lastPubTime': last_pub_time })
                coll_jobs.update(source_id, task_info)

            coll_task_history = self.db.collection('task_history')
            coll_task_history.store([{
                'sourceID': source_id,
                'task_sent_at': int(datetime.now().timestamp()),
                'status': success,
                'sourcePubTime':last_pub_time,
                'url': target_link
            }])
        
        self.db.commit()
        
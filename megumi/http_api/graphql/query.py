from graphene import (
    ObjectType,
    String,
    Field,
    DateTime,
    Int,
    Boolean,
    List
)
from graphql import GraphQLError
# from megumi.db import DAO, get_db
from megumi import db

# TODO: pagination

class Job(ObjectType):
    id = Int()
    name = String()
    description = String()
    url = String()
    # TODO: modify to DateTime type?
    lastPubTime = Int()
    addAt = Int()
    savePath = String()
    enable = Boolean()

    def __init__(self, *args, **kwargs):
        kwargs['id'] = kwargs['__id']
        del kwargs['__id']
        super().__init__(*args, **kwargs)


class TaskHistory(ObjectType):
    id = Int()
    sourceID = Int()
    sourcePubTime = Int()
    taskSentAt = Int()
    status = Int()
    link = String()
    
    def __init__(self, *args, **kwargs):
        kwargs['id'] = kwargs['__id']
        del kwargs['__id']
        super().__init__(*args, **kwargs)

class Query(ObjectType):
    job = List(Job, id=Int())
    task_history = List(TaskHistory, job_id=Int())

    def resolve_job(self, info, id=None):
        coll = db.get_db().collection('jobs')
        if id != None:
            data = coll.fetch(id)
            if data != None:
                data = [ coll.fetch(id) ]
            else:
                raise GraphQLError('Specified job not found')
        else:
            data = coll.all()
        return [Job(**d) for d in data]

    def resolve_task_history(self, info, job_id):
        # TODO
        pass

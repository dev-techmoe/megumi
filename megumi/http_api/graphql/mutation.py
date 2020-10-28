from graphene import (
    Mutation,
    ObjectType,
    Boolean,
    Int,
    InputObjectType,
    String
)
from graphql import GraphQLError
from megumi.db import DAO

class JobInputType(InputObjectType):
    name = String()
    description = String()
    url = String(required=True)
    enable = Boolean(default_value=True)
    savePath = String()

class CreateJob(Mutation):
    class Arguments:
        data = JobInputType()

    ok = Boolean()
    id = Int()

    def mutate(self, info, data: 'JobInputType'):
        job_id = DAO.get_instance().add_job(dict(data))
        return CreateJob(ok=True, id=job_id)

class DeleteJob(Mutation):
    class Arguments:
        id = Int(required=True)

    ok = Boolean()
    id = Int()

    def mutate(self, info, id):
        result = DAO.get_instance().delete_job(id)
        if not result:
            raise GraphQLError('Job not found')
        return DeleteJob(ok=True, id=id)

class UpdateJob(Mutation):
    class Arguments:
        id = Int(required=True)
        data = JobInputType(required=True)

    ok = Boolean()
    id = Int()

    def mutate(self, info, id, data):
        result = DAO.get_instance().update_job(id, dict(data))
        return UpdateJob(ok=result, id=id)

class RootMutation(ObjectType):
    create_job = CreateJob.Field()
    delete_job = DeleteJob.Field()
    update_job = UpdateJob.Field()
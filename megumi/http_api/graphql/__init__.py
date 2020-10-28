from .query import Query
from .mutation import RootMutation
from graphene import Schema

root_schema = Schema(query=Query, mutation=RootMutation)

__all__ = ['root_schema']
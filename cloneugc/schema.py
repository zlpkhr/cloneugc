import graphene

import cloneugc.api.schema


class Query(cloneugc.api.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)

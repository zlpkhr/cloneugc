import graphene
from graphene_django import DjangoObjectType

from cloneugc.api.models import Actor, Generation


class ActorType(DjangoObjectType):
    class Meta:
        model = Actor
        fields = "__all__"


class GenerationType(DjangoObjectType):
    class Meta:
        model = Generation
        fields = "__all__"


class Query(graphene.ObjectType):
    actors = graphene.List(ActorType)
    generations = graphene.List(GenerationType)

    def resolve_actors(self, info):
        return Actor.objects.all()

    def resolve_generations(self, info):
        return Generation.objects.all()


schema = graphene.Schema(query=Query)

import graphene
from graphene_django import DjangoObjectType

from cloneugc.api.models import Actor, Generation
from cloneugc.api.tasks import clone_actor


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


class CreateGenerationMutation(graphene.Mutation):
    class Arguments:
        actor_id = graphene.String(required=True)
        script = graphene.String(required=True)

    generation = graphene.Field(GenerationType)

    @classmethod
    def mutate(self, root, info, actor_id: str, script: str):
        actor = Actor.objects.get(id=actor_id)
        generation = Generation.objects.create(actor=actor)

        clone_actor.delay(generation.id, script)

        return CreateGenerationMutation(generation=generation)


class Mutation(graphene.ObjectType):
    create_generation = CreateGenerationMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

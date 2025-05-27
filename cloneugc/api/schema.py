import graphene
from django.core.cache import cache
from graphene_django import DjangoObjectType

from cloneugc.api.models import Actor, Generation
from cloneugc.api.tasks import clone_actor


class ActorType(DjangoObjectType):
    video_url = graphene.String()

    class Meta:
        model = Actor
        fields = ("id", "name", "created_at")

    def resolve_video_url(self, info):
        cache_key = f"actor_video_url_{self.id}"
        url = cache.get(cache_key)

        if url is None:
            url = self.video.url
            cache.set(cache_key, url, 600)

        return url


class GenerationType(DjangoObjectType):
    video_url = graphene.String()

    class Meta:
        model = Generation
        fields = ("id", "status", "created_at")

    def resolve_video_url(self, info):
        cache_key = f"generation_video_url_{self.id}"
        url = cache.get(cache_key)

        if url is None:
            url = self.video.url
            cache.set(cache_key, url, 600)

        return url


class Query(graphene.ObjectType):
    actors = graphene.List(ActorType)
    generations = graphene.List(GenerationType)
    actor = graphene.Field(ActorType, id=graphene.String())

    def resolve_actors(self, info):
        return Actor.objects.all()

    def resolve_generations(self, info):
        return Generation.objects.all()

    def resolve_actor(self, info, id):
        return Actor.objects.get(id=id)


class GenerationInput(graphene.InputObjectType):
    actor_id = graphene.String(required=True)
    script = graphene.String(required=True)


class CreateGenerationMutation(graphene.Mutation):
    class Arguments:
        input = GenerationInput(required=True)

    Output = GenerationType

    @classmethod
    def mutate(self, root, info, input: GenerationInput):
        actor = Actor.objects.get(id=input.actor_id)
        generation = Generation.objects.create(actor=actor)

        clone_actor.delay(generation.id, input.script)

        return generation


class Mutation(graphene.ObjectType):
    create_generation = CreateGenerationMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

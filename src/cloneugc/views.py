from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, View

from cloneugc.forms import ActorForm, VideoForm
from cloneugc.models import Actor, Generation
from cloneugc.tasks import clone_actor


def index(request: HttpRequest):
    return HttpResponse("Hello, World!")


class ActorListView(ListView):
    model = Actor
    context_object_name = "actors"


class ActorListCreateView(View):
    def get(self, request: HttpRequest):
        actors = Actor.objects.all().order_by("-created_at")

        return render(
            request,
            "cloneugc/actor_list.html",
            {"actors": actors, "url_name": request.resolver_match.url_name},
        )

    def post(self, request: HttpRequest):
        form = ActorForm(request.POST, request.FILES)

        form.save()

        return redirect(reverse_lazy("actor_list"))


class CreateVideoView(View):
    def get(self, request: HttpRequest):
        actor_id = request.GET.get("actor_id")

        if not actor_id:
            return HttpResponse("Bad Request", status=400)

        actor = get_object_or_404(Actor, id=actor_id)

        return render(request, "cloneugc/create_video.html", {"actor": actor})

    def post(self, request: HttpRequest):
        actor_id = request.GET.get("actor_id")

        if not actor_id:
            return HttpResponse("Bad Request", status=400)

        actor = get_object_or_404(Actor, id=actor_id)

        form = VideoForm(request.POST)

        if form.is_valid():
            gen = Generation.objects.create(
                actor=actor, status="Waiting for processing"
            )

            clone_actor.delay(gen.id, form.cleaned_data["script"])

            return redirect("actor_list")

        return HttpResponse("Unprocessable Entity", status=422)

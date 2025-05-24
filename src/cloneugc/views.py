from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, View

from cloneugc.forms import ActorForm
from cloneugc.models import Actor


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

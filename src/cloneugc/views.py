from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView

from cloneugc.models import Actor


def index(request: HttpRequest):
    return HttpResponse("Hello, World!")


class ActorListView(ListView):
    model = Actor
    context_object_name = "actors"

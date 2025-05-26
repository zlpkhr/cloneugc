import requests
from django.core.files.base import ContentFile
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import ListView, View

from cloneugc.api.forms import ActorForm, VideoForm
from cloneugc.api.models import Actor, Generation, GenerationStatus
from cloneugc.api.services import lipsyncer
from cloneugc.api.tasks import clone_actor


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
            gen = Generation.objects.create(actor=actor)

            clone_actor.delay(gen.id, form.cleaned_data["script"])

            return redirect("video_list")

        return HttpResponse("Unprocessable Entity", status=422)


@require_POST
@csrf_exempt
def lipsyncer_callback(request: HttpRequest):
    result = lipsyncer.callback_reader(request)

    gen = Generation.objects.get(lipsync_request_id=result["id"])

    gen.status = GenerationStatus.SAVING_VIDEO
    gen.save()

    response = requests.get(result["video_url"])

    # TODO: It might not be a mp4, but we don't care
    gen.video.save(f"{gen.actor.name}.mp4", ContentFile(response.content))

    gen.status = GenerationStatus.COMPLETED
    gen.save()

    return HttpResponse(status=204)


def generation(request: HttpRequest, id: str):
    gen = get_object_or_404(Generation, id=id)

    return JsonResponse(
        {
            "id": gen.id,
            "actor": gen.actor.name,
            "status": gen.status,
            "video": gen.video.url if gen.video else None,
            "audio": gen.audio.url if gen.audio else None,
            "lipsync_request_id": gen.lipsync_request_id,
        }
    )


class VideoListView(ListView):
    model = Generation
    context_object_name = "generations"
    template_name = "cloneugc/video_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["url_name"] = self.request.resolver_match.url_name

        return context

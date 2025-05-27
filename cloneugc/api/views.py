import requests
from django.core.files.base import ContentFile
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from cloneugc.api.forms import ActorForm
from cloneugc.api.models import Generation, GenerationStatus
from cloneugc.api.services import lipsyncer


@require_POST
@csrf_exempt
def lipsyncer_callback(request: HttpRequest):
    result = lipsyncer.callback_reader(request)

    gen = Generation.objects.get(lipsync_request_id=result["id"])

    gen.status = GenerationStatus.SAVING_VIDEO
    gen.save()

    response = requests.get(result["video_url"])

    # TODO: It might not be a mp4, but we don't care yet.
    gen.video.save(f"{gen.actor.name}.mp4", ContentFile(response.content))

    gen.status = GenerationStatus.COMPLETED
    gen.save()

    return HttpResponse(status=204)


@csrf_exempt
@require_POST
def create_actor(request: HttpRequest):
    form = ActorForm(request.POST, request.FILES)

    if form.is_valid():
        form.save()

        return JsonResponse({"id": form.instance.id})

    return HttpResponse("Unprocessable Entity", status=422)

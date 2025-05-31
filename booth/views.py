import requests
from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from .forms import PreviewAudioForm
from .models import Creator


@staff_member_required
def preview_audio(request: HttpRequest):
    form = PreviewAudioForm(request.GET)

    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=422)

    creator_id = form.cleaned_data["creator_id"]
    text = form.cleaned_data["text"]

    try:
        creator = Creator.objects.get(id=creator_id)
    except Creator.DoesNotExist:
        return JsonResponse({"errors": ["Creator not found"]}, status=404)

    if not creator.cartesia_voice_id:
        return JsonResponse(
            {"errors": ["No Cartesia voice ID for this creator"]}, status=400
        )

    try:
        resp = requests.post(
            "https://api.cartesia.ai/tts/bytes",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {settings.CARTESIA_API_KEY}",
                "Cartesia-Version": "2025-04-16",
            },
            json={
                "model_id": "sonic-2",
                "transcript": text,
                "voice": {
                    "mode": "id",
                    "id": creator.cartesia_voice_id,
                },
                "output_format": {
                    "container": "mp3",
                    "bit_rate": 128000,
                    "sample_rate": 44100,
                },
            },
            timeout=30,
        )

        resp.raise_for_status()
    except requests.RequestException as e:
        return JsonResponse({"errors": [str(e)]}, status=502)

    return HttpResponse(resp.content, content_type="audio/mpeg")

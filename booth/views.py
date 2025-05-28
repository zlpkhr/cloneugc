from django.http import HttpRequest, JsonResponse, HttpResponse
from django.conf import settings
from booth.forms import PreviewAudioForm
from booth.models import Creator
import requests


def preview_audio(request: HttpRequest):
    form = PreviewAudioForm(request.GET)

    if not form.is_valid():
        # Return the errors dictionary as is for validation errors
        return JsonResponse(form.errors, status=422)

    creator_id = form.cleaned_data["creator_id"]
    text = form.cleaned_data["text"]

    try:
        creator = Creator.objects.get(id=creator_id)
    except Creator.DoesNotExist:
        return JsonResponse({"error": "Creator not found."}, status=404)

    if not creator.cartesia_voice_id:
        return JsonResponse(
            {"error": "No Cartesia voice ID for this creator."}, status=400
        )

    url = "https://api.cartesia.ai/tts/bytes"
    headers = {
        "Cartesia-Version": "2025-04-16",
        "Authorization": f"Bearer {settings.CARTESIA_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
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
        }
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=502)

    return HttpResponse(resp.content, content_type="audio/mpeg")

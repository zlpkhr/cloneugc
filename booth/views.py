from django.shortcuts import render
import base64

import requests
from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_GET

from .cv import generate_aruco_board_img
from .forms import ArucoBoardImgForm, PreviewAudioForm
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


def aruco_board(request: HttpRequest):
    return render(request, "booth/aruco_board.html")


@require_GET
def aruco_board_img(request: HttpRequest):
    form = ArucoBoardImgForm(request.GET)

    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=422)

    screen_width = form.cleaned_data["screen_width"]
    screen_height = form.cleaned_data["screen_height"]

    light_img, dark_img = generate_aruco_board_img(screen_width, screen_height)

    light_b64 = base64.b64encode(light_img).decode("ascii")
    dark_b64 = base64.b64encode(dark_img).decode("ascii")
    return JsonResponse(
        {
            "light": light_b64,
            "dark": dark_b64,
        }
    )

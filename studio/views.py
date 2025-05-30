import json
from django.conf import settings
import requests
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from booth.models import Creator
from .ai import format_sonic_text
from .models import Ugc
from .forms import UgcForm
from .tasks import create_ugc_video


class CreateUgcView(CreateView):
    model = Ugc
    form_class = UgcForm
    template_name = "studio/ugc_form.html"
    success_url = reverse_lazy("create_ugc")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["creators"] = Creator.objects.all()
        ctx["ugcs"] = Ugc.objects.all().order_by("-created_at")

        return ctx

    def form_valid(self, form):
        response = super().form_valid(form)
        create_ugc_video.delay(self.object.id)
        return response


@csrf_exempt
@require_POST
def prepare_script(request: HttpRequest):
    payload = json.loads(request.body)
    script = payload.get("script")

    if len(script) == 0:
        return JsonResponse({"error": "A script is required."}, status=422)

    prepared_script = format_sonic_text(script)

    return JsonResponse({"preparedScript": prepared_script})


@csrf_exempt
@require_POST
def preview_audio(request: HttpRequest):
    payload = json.loads(request.body)

    creator_id = payload.get("creator_id")
    text = payload.get("text")

    if not creator_id:
        return JsonResponse({"error": "Creator ID is required"}, status=422)

    if not text:
        return JsonResponse({"error": "Text is required"}, status=422)

    try:
        creator = Creator.objects.get(id=creator_id)
    except Creator.DoesNotExist:
        return JsonResponse({"error": "Creator not found"}, status=404)

    if not creator.cartesia_voice_id:
        return JsonResponse(
            {"error": "No Cartesia voice ID for this creator"}, status=400
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
        return JsonResponse({"error": str(e)}, status=502)

    return HttpResponse(resp.content, content_type="audio/mpeg")

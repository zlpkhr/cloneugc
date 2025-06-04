import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView

from apps.booth.models import Creator
from apps.voicecloner import default_voicecloner

from .forms import UgcForm
from .models import Ugc
from .tasks import create_ugc_video


class CreateUgcView(LoginRequiredMixin, CreateView):
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
        account = self.request.user.account

        account.credits -= 1
        account.save()

        form.instance.account = account
        response = super().form_valid(form)

        create_ugc_video.delay(self.object.id)
        return response


@csrf_exempt
@require_POST
@login_required
def prepare_script(request: HttpRequest):
    payload = json.loads(request.body)
    script = payload.get("script")

    if len(script) == 0:
        return JsonResponse({"error": "A script is required."}, status=422)

    prepared_script = default_voicecloner.format_text(script)

    return JsonResponse({"preparedScript": prepared_script})


@csrf_exempt
@require_POST
@login_required
def preview_speech(request: HttpRequest):
    payload = json.loads(request.body)

    creator_id = payload.get("creatorId")
    text = payload.get("text")

    validation_errs = []

    if not creator_id:
        validation_errs.append("Creator ID is required.")

    if not text:
        validation_errs.append("Text is required.")

    if validation_errs:
        return JsonResponse({"errors": validation_errs}, status=422)

    try:
        creator = Creator.objects.get(id=creator_id)
    except Creator.DoesNotExist:
        return JsonResponse({"errors": ["Creator was not found."]}, status=404)

    if not creator.cartesia_voice_id:
        return JsonResponse(
            {"errors": ["No Cartesia voice ID for this creator."]}, status=500
        )

    try:
        resp = default_voicecloner.tts(
            creator.cartesia_voice_id,
            text,
        )
    except Exception as e:
        return JsonResponse({"errors": [str(e)]}, status=502)

    return HttpResponse(resp, content_type="audio/mpeg")

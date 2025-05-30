import json
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, JsonResponse
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

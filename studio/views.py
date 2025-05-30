from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from booth.models import Creator
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

        return ctx

    def form_valid(self, form):
        response = super().form_valid(form)
        create_ugc_video.delay(self.object.id)
        return response

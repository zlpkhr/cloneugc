from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Ugc
from .forms import UgcForm
from .tasks import create_ugc_video


class CreateUgcView(CreateView):
    model = Ugc
    form_class = UgcForm
    template_name = "studio/ugc_form.html"
    success_url = reverse_lazy("create_ugc")

    def form_valid(self, form):
        response = super().form_valid(form)
        create_ugc_video.delay(self.object.id)
        return response

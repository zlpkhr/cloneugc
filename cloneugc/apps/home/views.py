from urllib.parse import urlencode

from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from .forms import ContactForm


def home(request: HttpRequest):
    return render(request, "home/home.html")


class CreateContactView(View):
    def post(self, request: HttpRequest):
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            contact_saved = True
        else:
            contact_saved = False

        return redirect(
            reverse("home")
            + "?"
            + urlencode({"contact_saved": contact_saved})
            + "#contact"
        )

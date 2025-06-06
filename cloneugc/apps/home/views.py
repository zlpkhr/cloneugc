from urllib.parse import urlencode

from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from apps.notion import databases

from .forms import ContactForm


def home(request: HttpRequest):
    return render(request, "home/home.html")


class CreateContactView(View):
    contacts_db = databases["Contacts"]

    def post(self, request: HttpRequest):
        form = ContactForm(request.POST)

        if form.is_valid():
            contact_saved = self.contacts_db.insert(
                {
                    "Name": form.cleaned_data["name"],
                    "Email": form.cleaned_data["email"],
                    "App Details": form.cleaned_data["app_details"],
                }
            )
        else:
            contact_saved = False

        return redirect(
            reverse("home")
            + "?"
            + urlencode({"contact_saved": contact_saved})
            + "#contact"
        )

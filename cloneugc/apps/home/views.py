from urllib.parse import urlencode

from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from lib.notion import Database
from notion_client import Client

from .forms import ContactForm


def home(request: HttpRequest):
    return render(request, "home/home.html")


class CreateContactView(View):
    notion = Client(auth=settings.NOTION["integration_token"])
    contacts_db = Database(
        notion,
        settings.NOTION["databases"]["Contacts"]["id"],
    )

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

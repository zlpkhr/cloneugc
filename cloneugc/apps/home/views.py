from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ContactForm


def home(request: HttpRequest):
    return render(request, "home/home.html")


def save_contact(request: HttpRequest):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()

    return redirect(reverse("home") + "?contact_saved=true")

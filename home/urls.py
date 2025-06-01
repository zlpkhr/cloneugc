from django.urls import path

from home.views import home, save_contact

urlpatterns = [
    path("", home, name="home"),
    path("save-contact/", save_contact, name="save_contact"),
]
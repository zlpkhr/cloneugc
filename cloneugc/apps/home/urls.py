from django.urls import path

from .views import CreateContactView, home

urlpatterns = [
    path("", home, name="home"),
    path("contacts/", CreateContactView.as_view(), name="create_contact"),
]

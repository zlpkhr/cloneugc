from django.urls import path

from cloneugc import views

urlpatterns = [
    path("", views.index, name="index"),
]

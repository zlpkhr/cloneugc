from django.urls import path

from cloneugc.api import views

urlpatterns = [
    path("lipsyncer/callback", views.lipsyncer_callback, name="lipsyncer_callback"),
    path("api/actors/create/", views.create_actor, name="create_actor"),
]

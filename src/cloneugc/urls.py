from django.urls import path

from cloneugc import views

urlpatterns = [
    path("", views.index, name="index"),
    path("actors/", views.ActorListCreateView.as_view(), name="actor_list"),
]

from django.urls import path

from cloneugc import views

urlpatterns = [
    path("", views.index, name="index"),
    path("actors/", views.ActorListView.as_view(), name="actor_list"),
    path("actors/create/", views.ActorCreateView.as_view(), name="actor_create"),
]

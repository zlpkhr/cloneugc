from django.urls import path

from cloneugc.api import views

urlpatterns = [
    path("actors/", views.ActorListCreateView.as_view(), name="actor_list"),
    path("videos/create", views.CreateVideoView.as_view(), name="create_video"),
    path("lipsyncer/callback", views.lipsyncer_callback, name="lipsyncer_callback"),
    path("generations/<str:id>", views.generation, name="generation"),
    path("videos/", views.VideoListView.as_view(), name="video_list"),
    path("api/actors/create/", views.create_actor, name="create_actor"),
]

from django.urls import path

from .views import preview_audio

urlpatterns = [
    path("preview-audio", preview_audio, name="preview-audio"),
]

from django.urls import path

from .views import CreateUgcView, prepare_script, preview_speech

urlpatterns = [
    path("create/", CreateUgcView.as_view(), name="create_ugc"),
    path("prepare-script/", prepare_script, name="prepare_script"),
    path("preview-speech/", preview_speech, name="preview_speech"),
]

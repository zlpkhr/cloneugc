from django.urls import path

from .views import CreateUgcView

urlpatterns = [
    path("create/", CreateUgcView.as_view(), name="create_ugc"),
]

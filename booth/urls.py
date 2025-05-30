from django.urls import path

from booth.views import aruco_board, aruco_board_img, preview_audio

urlpatterns = [
    path("preview-audio", preview_audio, name="preview-audio"),
    path("aruco-board", aruco_board, name="aruco-board"),
    path("aruco-board-img", aruco_board_img, name="aruco-board-img"),
]

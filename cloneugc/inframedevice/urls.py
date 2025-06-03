from django.urls import path

from inframedevice.views import aruco_board, aruco_board_img

urlpatterns = [
    path("aruco-board", aruco_board, name="aruco-board"),
    path("aruco-board-img", aruco_board_img, name="aruco-board-img"),
]

import base64

from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from inframedevice.cv import generate_aruco_board_img
from inframedevice.forms import ArucoBoardImgForm


def aruco_board(request: HttpRequest):
    return render(request, "inframedevice/aruco_board.html")


@require_GET
def aruco_board_img(request: HttpRequest):
    form = ArucoBoardImgForm(request.GET)

    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=422)

    screen_width = form.cleaned_data["screen_width"]
    screen_height = form.cleaned_data["screen_height"]

    light_img, dark_img = generate_aruco_board_img(screen_width, screen_height)

    light_b64 = base64.b64encode(light_img).decode("ascii")
    dark_b64 = base64.b64encode(dark_img).decode("ascii")
    return JsonResponse(
        {
            "light": light_b64,
            "dark": dark_b64,
        }
    )

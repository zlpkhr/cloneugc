import cv2
import numpy as np


def generate_aruco_board_img(
    screen_width: int,
    screen_height: int,
):
    # Calculate the aspect ratio from the provided dimensions
    aspect_ratio = screen_width / screen_height

    # Calculate the largest board that fits the aspect ratio within the screen
    if screen_width / aspect_ratio <= screen_height:
        board_w = screen_width
        board_h = int(screen_width / aspect_ratio)
    else:
        board_h = screen_height
        board_w = int(screen_height * aspect_ratio)

    marker_size = 80  # pixels
    margin = 10  # pixels from edge (set to 0 if you want no margin)
    marker_ids = [0, 1, 2, 3]
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

    # Create blank white board
    board = np.ones((board_h, board_w), dtype=np.uint8) * 255

    # Corner positions: (top-left, top-right, bottom-right, bottom-left)
    positions = [
        (margin, margin),
        (board_w - margin - marker_size, margin),
        (board_w - margin - marker_size, board_h - margin - marker_size),
        (margin, board_h - margin - marker_size),
    ]

    # Draw markers
    for i, (x, y) in enumerate(positions):
        marker = np.zeros((marker_size, marker_size), dtype=np.uint8)
        cv2.aruco.generateImageMarker(dictionary, marker_ids[i], marker_size, marker)
        board[y : y + marker_size, x : x + marker_size] = marker

    success, buf = cv2.imencode(".png", board)
    if not success:
        raise RuntimeError("Failed to encode image")
    return buf.tobytes()

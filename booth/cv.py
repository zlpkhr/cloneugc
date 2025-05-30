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

    # Calculate marker size relative to screen dimensions
    # We want good margins and spacing between markers while maximizing marker size
    # Target: margin should be at least 8% of dimension, space between markers at least 15%
    min_margin_percent = 0.08  # 8% minimum margin from edges
    min_space_percent = 0.15  # 15% minimum space between markers

    # Calculate maximum marker size based on width constraint
    # Width layout: margin + marker + space + marker + margin
    available_width = board_w * (1 - 2 * min_margin_percent - min_space_percent)
    marker_size_from_width = int(available_width / 2)

    # Calculate maximum marker size based on height constraint
    # Height layout: margin + marker + space + marker + margin
    available_height = board_h * (1 - 2 * min_margin_percent - min_space_percent)
    marker_size_from_height = int(available_height / 2)

    # Use the smaller of the two to ensure both constraints are met
    marker_size = min(marker_size_from_width, marker_size_from_height)

    # Ensure minimum marker size for readability
    marker_size = max(marker_size, 40)

    # Calculate actual margins to center everything nicely
    margin_w = int((board_w - 2 * marker_size) * 0.25)  # 25% of remaining space
    margin_h = int((board_h - 2 * marker_size) * 0.25)  # 25% of remaining space

    # Use the smaller margin to maintain consistent spacing
    margin = min(margin_w, margin_h)

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

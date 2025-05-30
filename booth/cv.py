import cv2
import numpy as np
import json


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

    # Create metadata for QR code
    metadata = {
        "dictionary": "DICT_4X4_50",
        "marker_size_px": marker_size,
        "margin_px": margin,
        "corner_markers": {
            "TL": {"id": 0, "corner_index": 0},
            "TR": {"id": 1, "corner_index": 1},
            "BR": {"id": 2, "corner_index": 2},
            "BL": {"id": 3, "corner_index": 3}
        },
        "screen_aspect": round(aspect_ratio, 3)
    }

    # Calculate QR code size - make it as large as possible without overlapping markers
    # QR code will be placed in the center, so we need to ensure it doesn't reach the markers
    center_x, center_y = board_w // 2, board_h // 2

    # Calculate the minimum distance from center to any marker
    marker_positions = [
        (margin + marker_size // 2, margin + marker_size // 2),  # TL
        (board_w - margin - marker_size // 2, margin + marker_size // 2),  # TR
        (board_w - margin - marker_size // 2, board_h - margin - marker_size // 2),  # BR
        (margin + marker_size // 2, board_h - margin - marker_size // 2),  # BL
    ]

    min_distance_to_marker = float('inf')
    for mx, my in marker_positions:
        distance = min(abs(center_x - mx), abs(center_y - my))
        min_distance_to_marker = min(min_distance_to_marker, distance)

    # QR code should be smaller than twice the minimum distance (with some safety margin)
    qr_safety_margin = 20  # pixels
    max_qr_size = int((min_distance_to_marker - qr_safety_margin) * 2)
    max_qr_size = max(max_qr_size, 80)  # Minimum QR code size for readability

    # Generate QR code using OpenCV
    qr_encoder = cv2.QRCodeEncoder.create()
    metadata_json = json.dumps(metadata, separators=(',', ':'))
    
    # Generate QR code image
    qr_img = qr_encoder.encode(metadata_json)
    
    # Convert to grayscale if needed and resize to fit the calculated size
    if len(qr_img.shape) == 3:
        qr_img = cv2.cvtColor(qr_img, cv2.COLOR_BGR2GRAY)
    
    # Scale QR code to fit the calculated size
    qr_height, qr_width = qr_img.shape
    scale_factor = min(max_qr_size / qr_width, max_qr_size / qr_height)
    new_qr_width = int(qr_width * scale_factor)
    new_qr_height = int(qr_height * scale_factor)
    
    # Resize QR code using nearest neighbor to maintain sharpness
    qr_resized = cv2.resize(qr_img, (new_qr_width, new_qr_height), interpolation=cv2.INTER_NEAREST)

    # Create blank white board
    board = np.ones((board_h, board_w), dtype=np.uint8) * 255

    # Corner positions: (top-left, top-right, bottom-right, bottom-left)
    positions = [
        (margin, margin),
        (board_w - margin - marker_size, margin),
        (board_w - margin - marker_size, board_h - margin - marker_size),
        (margin, board_h - margin - marker_size),
    ]

    # Draw ArUco markers
    for i, (x, y) in enumerate(positions):
        marker = np.zeros((marker_size, marker_size), dtype=np.uint8)
        cv2.aruco.generateImageMarker(dictionary, marker_ids[i], marker_size, marker)
        board[y : y + marker_size, x : x + marker_size] = marker

    # Place QR code in the center
    qr_start_x = center_x - new_qr_width // 2
    qr_start_y = center_y - new_qr_height // 2
    qr_end_x = qr_start_x + new_qr_width
    qr_end_y = qr_start_y + new_qr_height
    
    # Ensure QR code fits within board boundaries
    qr_start_x = max(0, qr_start_x)
    qr_start_y = max(0, qr_start_y)
    qr_end_x = min(board_w, qr_end_x)
    qr_end_y = min(board_h, qr_end_y)
    
    # Place the QR code
    board[qr_start_y:qr_end_y, qr_start_x:qr_end_x] = qr_resized[:qr_end_y-qr_start_y, :qr_end_x-qr_start_x]

    success, buf = cv2.imencode(".png", board)
    if not success:
        raise RuntimeError("Failed to encode image")
    return buf.tobytes()

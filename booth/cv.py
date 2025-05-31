import cv2
import numpy as np
import json
import qrcode
from PIL import Image  # qrcode returns a PIL image


def generate_aruco_board_img(screen_width: int, screen_height: int):
    # ---------- 1. BOARD SIZE ----------
    aspect_ratio = screen_width / screen_height
    if screen_width / aspect_ratio <= screen_height:
        board_w = screen_width
        board_h = int(screen_width / aspect_ratio)
    else:
        board_h = screen_height
        board_w = int(screen_height * aspect_ratio)

    # ---------- 2. MARKER SIZE ----------
    min_margin_percent, min_space_percent = 0.08, 0.15
    marker_size = min(
        int(board_w * (1 - 2 * min_margin_percent - min_space_percent) / 2),
        int(board_h * (1 - 2 * min_margin_percent - min_space_percent) / 2),
    )
    marker_size = max(marker_size, 40)

    # ---------- 3. MARGINS ----------
    margin_w = int((board_w - 2 * marker_size) * 0.25)
    margin_h = int((board_h - 2 * marker_size) * 0.25)
    margin = min(margin_w, margin_h)

    # ---------- 4. METADATA ----------
    metadata = {
        "dictionary": "DICT_4X4_50",
        "marker_size_px": marker_size,
        "margin_px": margin,
        "corner_markers": {
            "TL": {"id": 0, "corner_index": 0},
            "TR": {"id": 1, "corner_index": 1},
            "BR": {"id": 2, "corner_index": 2},
            "BL": {"id": 3, "corner_index": 3},
        },
        "screen_aspect": round(aspect_ratio, 3),
    }
    metadata_json = json.dumps(metadata, separators=(",", ":"))

    # ---------- 5. QR-CODE SIZE ----------
    center_x, center_y = board_w // 2, board_h // 2
    marker_centres = [
        (margin + marker_size // 2, margin + marker_size // 2),  # TL
        (board_w - margin - marker_size // 2, margin + marker_size // 2),  # TR
        (
            board_w - margin - marker_size // 2,
            board_h - margin - marker_size // 2,
        ),  # BR
        (margin + marker_size // 2, board_h - margin - marker_size // 2),  # BL
    ]
    min_dist = min(
        min(abs(center_x - mx), abs(center_y - my)) for mx, my in marker_centres
    )
    qr_side = max(int((min_dist - 20) * 2), 80)  # keep ≥80 px

    # ---------- 6. QR-CODE GENERATION (qrcode) ----------
    # ----- where you build the QR object -----
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # ← bump to H
        box_size=2,  # ← each module starts at 2 px, gives more headroom
        border=4,  # ← full quiet zone (spec minimum)
    )

    qr.add_data(metadata_json)
    qr.make(fit=True)

    qr_img_pil = qr.make_image(fill_color="black", back_color="white").convert("L")
    qr_img_np = np.array(qr_img_pil)

    # upscale/downscale to fit qr_side, keeping hard edges
    qr_img_np = cv2.resize(
        qr_img_np,
        (qr_side, qr_side),
        interpolation=cv2.INTER_NEAREST,
    )

    # ---------- 7. BOARD CANVAS ----------
    board_dark = np.ones((board_h, board_w), dtype=np.uint8) * 255  # white bg

    # four marker placements (TL, TR, BR, BL)
    corner_positions = [
        (margin, margin),
        (board_w - margin - marker_size, margin),
        (board_w - margin - marker_size, board_h - margin - marker_size),
        (margin, board_h - margin - marker_size),
    ]
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    for idx, (x, y) in enumerate(corner_positions):
        marker = np.zeros((marker_size, marker_size), dtype=np.uint8)
        cv2.aruco.generateImageMarker(dictionary, idx, marker_size, marker)
        board_dark[y : y + marker_size, x : x + marker_size] = marker

    # place QR centred
    xs, ys = center_x - qr_side // 2, center_y - qr_side // 2
    board_dark[ys : ys + qr_side, xs : xs + qr_side] = qr_img_np

    # ---------- 8. LIGHT MODE ----------
    board_light = 255 - board_dark

    ok_light, buf_light = cv2.imencode(".png", board_light)
    ok_dark, buf_dark = cv2.imencode(".png", board_dark)
    if not (ok_light and ok_dark):
        raise RuntimeError("PNG encoding failed")

    return buf_light.tobytes(), buf_dark.tobytes()

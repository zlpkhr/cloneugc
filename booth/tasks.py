import os
import subprocess
import tempfile

from celery import shared_task
from django.core.files.storage import default_storage

from booth.models import Creator
from shortid import shortid


@shared_task
def convert_video_to_mp4(creator_id: str):
    creator = Creator.objects.get(id=creator_id)

    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmpfile:
        output_video_path = tmpfile.name

    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-i",
        creator.video_url,
        "-c:v",
        "libx264",
        "-preset",
        "fast",
        "-crf",
        "23",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        "-movflags",
        "+faststart",
        "-pix_fmt",
        "yuv420p",
        output_video_path,
    ]

    try:
        subprocess.run(
            ffmpeg_cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as err:
        if os.path.exists(output_video_path):
            os.remove(output_video_path)

        err_msg = err.stderr.decode("utf-8").strip() if err.stderr else "Unknown error"
        raise Exception(f"FFmpeg failed: {err_msg}")

    try:
        with open(output_video_path, "rb") as file:
            saved_path = default_storage.save(
                f"{Creator.video_mp4_upload_to}/{shortid()}.mp4", file
            )

        creator.video_mp4.name = saved_path
        creator.save()

        return saved_path
    finally:
        if os.path.exists(output_video_path):
            os.remove(output_video_path)

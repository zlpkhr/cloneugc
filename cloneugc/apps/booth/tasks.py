import logging
import os
import subprocess
import tempfile

from celery import shared_task
from django.core.files.storage import default_storage
from lib.shortid import shortid

from apps.voicecloner import default_voicecloner

from .models import Creator

logger = logging.getLogger(__name__)


@shared_task(acks_late=True)
def convert_video_to_mp4(creator_id: str):
    creator = Creator.objects.get(id=creator_id)

    ffprobe_cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=format_name",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        creator.video.url,
    ]

    try:
        result = subprocess.run(
            ffprobe_cmd,
            text=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        formats = result.stdout.strip().split(",")
        logger.info(
            f"FFprobe ran successfully for creator {creator.name} ({creator.id})."
        )
        if "mp4" in formats:
            logger.info(
                f"Creator {creator.name} ({creator.id}) video is already in mp4 format."
            )
            creator.video_mp4.name = creator.video.name
            creator.save()
            return

        logger.info(
            f"Creator {creator.name} ({creator.id}) does not have an mp4 video."
        )
    except subprocess.CalledProcessError as err:
        err_msg = err.stderr.decode("utf-8").strip() if err.stderr else "Unknown error"
        logger.error(
            f"FFprobe failed for creator {creator.name} ({creator.id}): {err_msg}"
        )

    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmpfile:
        output_video_path = tmpfile.name

    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-i",
        creator.video.url,
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
        logger.info(
            f"FFmpeg ran successfully for creator {creator.name} ({creator.id})."
        )
    except subprocess.CalledProcessError as err:
        if os.path.exists(output_video_path):
            os.remove(output_video_path)

        err_msg = err.stderr.decode("utf-8").strip() if err.stderr else "Unknown error"
        logger.error(
            f"FFmpeg failed for creator {creator.name} ({creator.id}): {err_msg}"
        )
        raise Exception(f"FFmpeg failed: {err_msg}")

    try:
        with open(output_video_path, "rb") as file:
            saved_path = default_storage.save(
                f"{Creator.video_mp4_upload_to}/{shortid()}.mp4", file
            )

        creator.video_mp4.name = saved_path
        creator.save()

        logger.info(
            f'Saved converted video for creator {creator.name} ({creator.id}) at "{saved_path}".'
        )

        return saved_path
    finally:
        if os.path.exists(output_video_path):
            os.remove(output_video_path)
        logger.debug(
            f"Removed temporary file {output_video_path} for creator {creator.name} ({creator.id})."
        )


@shared_task(acks_late=True)
def create_voice_clone(creator_id: str):
    creator = Creator.objects.get(id=creator_id)

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmpfile:
        audio_path = tmpfile.name

    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-i",
        creator.video_url,
        "-vn",
        "-acodec",
        "libmp3lame",
        "-ar",
        "44100",
        "-ac",
        "2",
        "-b:a",
        "192k",
        audio_path,
    ]

    try:
        subprocess.run(
            ffmpeg_cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        logger.info(f"Extracted audio for creator {creator.name} ({creator.id})")
    except subprocess.CalledProcessError as err:
        if os.path.exists(audio_path):
            os.remove(audio_path)
        err_msg = err.stderr.decode("utf-8").strip() if err.stderr else "Unknown error"
        logger.error(
            f"FFmpeg audio extraction failed for creator {creator.name} ({creator.id}): {err_msg}"
        )
        raise Exception(f"FFmpeg audio extraction failed: {err_msg}")

    name = f"{creator.name} ({creator.id})"
    language = creator.language

    with open(audio_path, "rb") as audio_file:
        voice_id = default_voicecloner.clone_voice(name, language, audio_file.read())

    if os.path.exists(audio_path):
        os.remove(audio_path)
        logger.debug(f"Removed temporary audio file {audio_path}")

    creator.cartesia_voice_id = voice_id
    creator.save()
    logger.info(
        f"Voice clone created and saved for creator {creator.name} ({creator.id}), voice id: {voice_id}"
    )

import logging
import os
import subprocess
import tempfile

import requests
from celery import shared_task
from django.conf import settings
from django.core.files.storage import default_storage

from .models import Creator
from shortid import shortid

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

    url = "https://api.cartesia.ai/voices/clone"
    headers = {
        "Cartesia-Version": "2025-04-16",
        "Authorization": f"Bearer {settings.CARTESIA_API_KEY}",
    }
    name = f"{creator.name} ({creator.id})"
    language = creator.language

    with open(audio_path, "rb") as audio_file:
        files = {"clip": (f"{creator.id}.mp3", audio_file, "audio/mpeg")}
        data = {
            "name": name,
            "language": language,
        }
        response = requests.post(url, data=data, files=files, headers=headers)

    if os.path.exists(audio_path):
        os.remove(audio_path)
        logger.debug(f"Removed temporary audio file {audio_path}")

    response.raise_for_status()

    result = response.json()
    voice_id = result.get("id")
    if voice_id:
        creator.cartesia_voice_id = voice_id
        creator.save()
        logger.info(
            f"Voice clone created and saved for creator {creator.name} ({creator.id}), voice id: {voice_id}"
        )
        return result
    else:
        raise Exception(
            f"Voice clone API succeeded but no id returned for creator {creator.name} ({creator.id})"
        )


@shared_task(acks_late=True)
def delete_cartesia_voice(voice_id: str):
    """
    Deletes a Cartesia voice by its ID using the Cartesia API.
    Logs any errors that occur.
    """
    url = f"https://api.cartesia.ai/voices/{voice_id}"
    headers = {
        "Cartesia-Version": "2025-04-16",
        "Authorization": f"Bearer {settings.CARTESIA_API_KEY}",
    }
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        logger.info(f"Successfully deleted Cartesia voice {voice_id}")
    except Exception as e:
        logger.error(f"Failed to delete Cartesia voice {voice_id}: {e}")
        if hasattr(e, "response") and e.response is not None:
            logger.error(f"Response content: {e.response.text}")
        return None

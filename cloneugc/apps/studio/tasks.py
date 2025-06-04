import json
import logging
from pathlib import Path

import requests
from celery import shared_task
from django.conf import settings
from django.core.files.base import ContentFile
from lib.shortid import shortid

from apps.voicecloner import default_voicecloner

from .models import Ugc

logger = logging.getLogger(__name__)


@shared_task(acks_late=True)
def create_ugc_video(ugc_id: str):
    ugc = Ugc.objects.select_related("creator").get(id=ugc_id)

    if not ugc.creator:
        raise Exception(f"UGC {ugc_id} has no creator")
    if not ugc.creator.cartesia_voice_id:
        raise Exception(f"UGC {ugc_id} has no Cartesia voice ID")

    tts_resp = default_voicecloner.tts(ugc.creator.cartesia_voice_id, ugc.script)
    ugc.audio.save(f"{ugc.id}.mp3", ContentFile(tts_resp))
    logger.info("Saved audio")
    ugc.save()

    submit_resp = requests.post(
        "https://queue.fal.run/fal-ai/sync-lipsync/v2",
        headers={
            "Authorization": f"Key {settings.FAL_API_KEY}",
        },
        json={
            "video_url": ugc.creator.video_url,
            "audio_url": ugc.audio.url,
            "sync_mode": "bounce",
        },
        timeout=60,
    )
    submit_resp.raise_for_status()
    submit_data = submit_resp.json()
    request_id = submit_data.get("request_id")
    if not request_id:
        raise Exception("Fal API did not return a request id")

    status_stream_url = (
        f"https://queue.fal.run/fal-ai/sync-lipsync/requests/{request_id}/status/stream"
    )
    with requests.get(
        status_stream_url,
        headers={
            "Authorization": f"Key {settings.FAL_API_KEY}",
        },
        stream=True,
        timeout=600,
    ) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines():
            if not line or line.startswith(b":"):
                continue  # skip keepalive or comments
            try:
                data = json.loads(line.lstrip(b"data: ").decode("utf-8"))
            except Exception:
                continue
            status = data.get("status", "").upper()
            logger.info(f"Status: {status}")
            if status == "COMPLETED":
                break
            elif status == "FAILED":
                raise Exception(
                    f"Fal lipsync job failed: {data}, request_id: {request_id}"
                )

    result_url = f"https://queue.fal.run/fal-ai/sync-lipsync/requests/{request_id}"
    logger.info(f"Result URL: {result_url}")
    result_resp = requests.get(
        result_url,
        headers={
            "Authorization": f"Key {settings.FAL_API_KEY}",
        },
        timeout=60,
    )
    result_resp.raise_for_status()
    result_data = result_resp.json()
    video_file_url = result_data["video"]["url"]
    video_content_resp = requests.get(video_file_url, timeout=600)
    video_content_resp.raise_for_status()
    filename = result_data["video"]["file_name"]
    path = Path(filename)
    fn = shortid() + path.suffix
    ugc.video.save(fn, ContentFile(video_content_resp.content))
    logger.info("Saved video")
    ugc.save()

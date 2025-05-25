import json

import requests
from django.conf import settings
from django.http import HttpRequest


class Cartesia:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.version = "2025-05-25"

    def clone_voice(self, name: str, audio) -> str:
        response = requests.post(
            "https://api.cartesia.ai/voices/clone",
            headers={
                "Cartesia-Version": self.version,
                "Authorization": f"Bearer {self.api_key}",
            },
            files={"clip": audio},
            data={
                "name": name,
                "language": "en",
            },
        )
        response.raise_for_status()

        return response.json()["id"]

    def tts(self, voice_id: str, text: str):
        response = requests.post(
            "https://api.cartesia.ai/tts/bytes",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Cartesia-Version": self.version,
                "Content-Type": "application/json",
            },
            json={
                "model_id": "sonic-2",
                "transcript": text,
                "language": "en",
                "voice": {"id": voice_id},
                "output_format": {
                    "container": "mp3",
                    "bit_rate": 128000,
                    "sample_rate": 44100,
                },
            },
        )
        response.raise_for_status()

        return response.content


voice_cloner = Cartesia(settings.CARTESIA_API_KEY)


class FalSync:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def lipsync(self, video_url: str, audio_url: str, callback_url: str) -> str:
        response = requests.post(
            f"https://queue.fal.run/fal-ai/sync-lipsync/v2?fal_webhook={callback_url}",
            headers={
                "Authorization": f"Key {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "video_url": video_url,
                "audio_url": audio_url,
                "callback_url": callback_url,
            },
        )

        response.raise_for_status()

        return response.json()["request_id"]

    def callback_reader(self, request: HttpRequest) -> str:
        payload = json.loads(request.body)

        if payload["status"] != "OK":
            raise Exception(payload["error"])

        return {
            "id": payload["request_id"],
            "video_url": payload["video"]["url"],
        }


lipsyncer = FalSync(settings.FAL_API_KEY)

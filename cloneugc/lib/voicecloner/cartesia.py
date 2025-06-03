import logging

import httpx

from . import VoiceCloner


class Cartesia(VoiceCloner):
    def __init__(self, api_key: str):
        self.logger = logging.getLogger(__name__)
        self.client = httpx.Client(
            base_url="https://api.cartesia.ai",
            headers={
                "Cartesia-Version": "2025-04-16",
                "Authorization": f"Bearer {api_key}",
            },
        )

    def clone_voice(self, label: str, language: str, speech: bytes) -> str:
        response = self.client.post(
            "/voices/clone",
            data={"name": label, "language": language},
            files={"clip": ("speech.mp3", speech, "audio/mpeg")},
        )

        response.raise_for_status()

        result = response.json()
        voice_id = result.get("id")

        if not voice_id:
            self.logger.error(
                f"Voice clone API succeeded but no ID was returned: {result}"
            )
            raise Exception("Voice clone API succeeded but no ID was returned")

        return voice_id

    def tts(self, id: str, text: str) -> bytes:
        response = self.client.post(
            "/tts/bytes",
            json={
                "model_id": "sonic-2",
                "transcript": text,
                "voice": {
                    "mode": "id",
                    "id": id,
                },
                "output_format": {
                    "container": "mp3",
                    "bit_rate": 128000,
                    "sample_rate": 44100,
                },
            },
            timeout=90,
        )

        response.raise_for_status()

        return response.content

import requests
from django.conf import settings


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


voice_cloner = Cartesia(settings.CARTESIA_API_KEY)

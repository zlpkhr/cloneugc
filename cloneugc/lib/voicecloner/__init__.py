import logging
import random
import re
from abc import ABC, abstractmethod
from pathlib import Path

import httpx

from lib.llm import LLM


class VoiceCloner(ABC):
    @abstractmethod
    def clone_voice(self, label: str, language: str, speech: bytes) -> str:
        """
        Create a new voice profile from an mp3 speech sample.
        Args:
            label: Name for the new voice.
            language: Language code of the sample (e.g., 'en').
            speech: MP3 audio data.
        Returns:
            Unique voice profile ID.
        """
        pass

    @abstractmethod
    def tts(self, id: str, text: str) -> bytes:
        """
        Generate mp3 audio from text using a voice profile.
        Args:
            id: Voice profile ID.
            text: Text to synthesize.
        Returns:
            MP3 audio bytes.
        """
        pass

    @abstractmethod
    def format_text(self, text: str) -> str:
        pass


PACKAGE_DIR = Path(__file__).resolve().parent


class Cartesia(VoiceCloner):
    def __init__(self, api_key: str, llm: LLM):
        self.logger = logging.getLogger(__name__)
        self.client = httpx.Client(
            base_url="https://api.cartesia.ai",
            headers={
                "Cartesia-Version": "2025-04-16",
                "Authorization": f"Bearer {api_key}",
            },
        )
        self.llm = llm

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

    format_text_prompt = open(PACKAGE_DIR / "cartesia_format_text.txt").read()

    def format_text(self, text: str) -> str:
        text = self.llm.transform_text(self.format_text_prompt, text)
        text = self.double_question_marks(text)
        text = self.insert_breaks(text)

        return text

    def double_question_marks(self, text: str) -> str:
        # Replace single question marks (not preceded or followed by another question mark) with double question marks
        return re.sub(r"(?<!\?)\?(?!\?)", "??", text)

    def insert_breaks(self, text: str) -> str:
        # Insert <break /> after exclamation marks at the end of sentences, but not if at end of text,
        # and only if there is not already a <break ...> tag after the exclamation mark.
        time = round(random.uniform(100, 300))
        # Match ! that is not followed by optional whitespace and a <break
        pattern = r"!(?=[\s\n](?!<break\b)(?!$))"
        return re.sub(pattern, rf'! <break time="{time}ms" />', text)


providers = {
    "cartesia": Cartesia,
}

__all__ = ["VoiceCloner", "providers"]

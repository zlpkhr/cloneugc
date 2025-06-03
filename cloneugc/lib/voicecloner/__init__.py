from abc import ABC, abstractmethod


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

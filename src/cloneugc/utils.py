import secrets
import subprocess
import tempfile
import urllib.parse

from django.conf import settings
from django.urls import reverse


def shortid(length=6):
    # Optimized for URL readability and UX:
    # - Removed visually similar: 0/o, 1/l, i, u
    # - Removed pronunciation issues: q (needs 'u'), x (uncommon)
    # - Kept vowels a,e for readability
    # - All remaining chars are keyboard-friendly and clear
    alphabet = "23456789abcdefghjkmnprstvwyz"  # 27 characters

    return "".join(secrets.choice(alphabet) for _ in range(length))


def extract_audio(video_url: str) -> str:
    """
    Uses ffmpeg to extract audio as mp3 from a remote video URL, outputs to a temp file, and returns the temp mp3 path.
    Caller is responsible for deleting the file.
    """
    # Prepare temp file for audio
    audio_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    audio_temp.close()

    # Run ffmpeg to extract audio as mp3 (192k bitrate, stereo, 44.1kHz)
    cmd = [
        "ffmpeg",
        "-y",  # overwrite output
        "-i",
        video_url,
        "-vn",  # no video
        "-acodec",
        "libmp3lame",
        "-ab",
        "192k",
        "-ar",
        "44100",
        "-ac",
        "2",
        audio_temp.name,
    ]
    subprocess.run(
        cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    return audio_temp.name


def reverse_absolute(*args, **kwargs):
    return urllib.parse.urljoin(settings.APP_URL, reverse(*args, **kwargs))

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from lib.voicecloner import VoiceCloner
from lib.voicecloner.providers import providers

if not settings.VOICE_CLONERS:
    raise ImproperlyConfigured("VOICE_CLONERS is not set")


voicecloners: dict[str, VoiceCloner] = {}

for name, config in settings.VOICE_CLONERS.items():
    provider = config.get("provider")

    if not provider:
        raise ImproperlyConfigured(f"VOICE_CLONERS[{name}] is missing a provider")

    if provider not in providers:
        raise ImproperlyConfigured(f"Unknown voice cloner provider: {provider}")

    voicecloners[name] = providers[provider](**config["options"])

default_voicecloner = voicecloners["default"]

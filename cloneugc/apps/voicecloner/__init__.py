from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string
from lib.voicecloner import VoiceCloner, providers

if not settings.VOICE_CLONERS:
    raise ImproperlyConfigured("VOICE_CLONERS is not set")


voicecloners: dict[str, VoiceCloner] = {}

for name, config in settings.VOICE_CLONERS.items():
    provider = config.get("provider")

    if not provider:
        raise ImproperlyConfigured(f"VOICE_CLONERS[{name}] is missing a provider")

    if provider not in providers:
        raise ImproperlyConfigured(f"Unknown voice cloner provider: {provider}")

    options = config.get("options", {}).copy()

    llm = options.get("llm")

    if isinstance(llm, str):
        options["llm"] = import_string(llm)

    voicecloners[name] = providers[provider](**options)

default_voicecloner = voicecloners["default"]

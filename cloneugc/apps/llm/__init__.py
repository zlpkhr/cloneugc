from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from lib.llm import LLM, providers

if not settings.LLM:
    raise ImproperlyConfigured("LLM is not set")

llms: dict[str, LLM] = {}

for name, config in settings.LLM.items():
    provider = config.get("provider")

    if not provider:
        raise ImproperlyConfigured(f"LLM[{name}] is missing a provider")

    if provider not in providers:
        raise ImproperlyConfigured(f"Unknown LLM provider: {provider}")

    llms[name] = providers[provider](**config["options"])

default_llm = llms["default"]

__all__ = ["llms", "default_llm"]

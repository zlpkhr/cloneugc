from abc import ABC, abstractmethod

from openai import Client


class LLM(ABC):
    @abstractmethod
    def transform_text(self, prompt: str, text: str) -> str:
        pass


class OAI(LLM):
    def __init__(self, api_key: str):
        self.client = Client(api_key=api_key)

    def transform_text(self, prompt: str, text: str) -> str:
        response = self.client.responses.create(
            model="gpt-4.1-nano-2025-04-14",
            instructions=prompt,
            input=text,
            store=True,
        )

        return response.output_text


providers = {
    "openai": OAI,
}

__all__ = ["LLM", "providers"]

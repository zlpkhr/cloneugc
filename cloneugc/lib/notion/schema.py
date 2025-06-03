from dataclasses import dataclass


@dataclass
class Text:
    value: str

    def serialize(self):
        return {"title": [{"text": {"content": self.value}}]}


@dataclass
class Email:
    value: str

    def serialize(self):
        return {"email": self.value}


@dataclass
class RichText:
    value: str

    def serialize(self):
        return {"rich_text": [{"text": {"content": self.value}}]}


schema = {
    "title": Text,
    "email": Email,
    "rich_text": RichText,
}

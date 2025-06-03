class Text:
    def __init__(self, value: str):
        self.value = value

    def serialize(self):
        return {"title": [{"text": {"content": self.value}}]}


class Email:
    def __init__(self, value: str):
        self.value = value

    def serialize(self):
        return {"email": self.value}

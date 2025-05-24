from django.db import models

from cloneugc.utils import shortid


def video_path(instance: "Actor", filename: str):
    return f"{instance.id}-{filename}"


class Actor(models.Model):
    id = models.CharField(
        primary_key=True, max_length=6, default=shortid, editable=False
    )
    name = models.CharField(max_length=100)
    video = models.FileField(upload_to=video_path)
    created_at = models.DateTimeField(auto_now_add=True)
    voice_id = models.TextField(null=True)

    def __str__(self):
        return self.name

    @property
    def voice_cloned(self) -> bool:
        return self.voice_id is not None

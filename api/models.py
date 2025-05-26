from django.db import models

from api.utils import shortid


def instance_path(instance: models.Model, filename: str):
    return f"{instance.pk}-{filename}"


class Actor(models.Model):
    id = models.CharField(
        primary_key=True, max_length=6, default=shortid, editable=False
    )
    name = models.CharField(max_length=100)
    video = models.FileField(upload_to=instance_path)
    created_at = models.DateTimeField(auto_now_add=True)
    voice_id = models.TextField(null=True)

    def __str__(self):
        return self.name

    @property
    def voice_cloned(self) -> bool:
        return self.voice_id is not None


class GenerationStatus(models.TextChoices):
    WAITING_PROCESSING = "waiting_processing", "Waiting Processing"
    CLONING_VOICE = "cloning_voice", "Cloning Voice"
    GENERATING_AUDIO = "generating_audio", "Generating Audio"
    SYNCING_LIPS = "syncing_lips", "Syncing Lips"
    SAVING_VIDEO = "saving_video", "Saving Video"
    COMPLETED = "completed", "Completed"


class Generation(models.Model):
    id = models.CharField(
        primary_key=True, max_length=6, default=shortid, editable=False
    )
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    audio = models.FileField(upload_to=instance_path, null=True)
    video = models.FileField(upload_to=instance_path, null=True)
    status = models.CharField(
        max_length=20,
        choices=GenerationStatus.choices,
        default=GenerationStatus.WAITING_PROCESSING,
    )
    lipsync_request_id = models.TextField(null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.actor.name} - {self.status}"

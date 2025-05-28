from django.contrib.postgres.fields import ArrayField
from django.db import models

from shortid import shortid


class Creator(models.Model):
    LANGUAGE_CHOICES = [
        ("en", "English"),
        ("ru", "Russian"),
    ]

    id = models.CharField(
        primary_key=True,
        max_length=6,
        default=shortid,
        editable=False,
    )
    name = models.CharField(max_length=64)
    tags = ArrayField(
        models.CharField(max_length=64),
        blank=True,
        default=list,
        help_text="Comma separated; leave blank if none.",
    )
    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        help_text="Changing language reclones voice.",
    )
    video = models.FileField(upload_to="booth/creators/videos")
    video_mp4 = models.FileField(
        null=True,
        blank=True,
        editable=False,
    )
    cartesia_voice_id = models.TextField(null=True, blank=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def video_url(self):
        return self.video_mp4.url if self.video_mp4 else self.video.url

    video_mp4_upload_to = "booth/creators/videos"

    def delete(self, *args, **kwargs):
        if self.cartesia_voice_id:
            from booth.tasks import delete_cartesia_voice  # Lazy import

            delete_cartesia_voice.delay(self.cartesia_voice_id)
        super().delete(*args, **kwargs)

from shortid import shortid
from django.core.cache import cache
from django.conf import settings
from django.db import models


class Creator(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=6,
        default=shortid,
        editable=False,
    )
    name = models.CharField(max_length=255)
    video = models.FileField(upload_to="booth/creators/videos")
    video_mp4 = models.FileField(
        null=True,
        blank=True,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def video_url(self):
        return self.video_mp4.url if self.video_mp4 else self.video.url

    video_mp4_upload_to = "booth/creators/videos"

from shortid import shortid
from django.db import models


class Creator(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=6,
        default=shortid,
        editable=False,
    )
    name = models.CharField(max_length=255)
    video = models.FileField(upload_to="booth/creators/videos/")
    video_mp4 = models.FileField(
        upload_to="booth/creators/videos/",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

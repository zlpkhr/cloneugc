from django.conf import settings
from django.core.cache import cache
from django.db import models

from accounts.models import Account
from apps.booth.models import Creator
from shortid import shortid


class Ugc(models.Model):
    class Meta:
        verbose_name = "UGC"
        verbose_name_plural = "UGCS"

    id = models.CharField(
        primary_key=True,
        max_length=6,
        default=shortid,
        editable=False,
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        editable=False,
    )
    creator = models.ForeignKey(Creator, null=True, on_delete=models.SET_NULL)
    audio = models.FileField(upload_to="ugc/audios/", null=True, blank=True)
    video = models.FileField(upload_to="ugc/videos/", null=True, blank=True)
    script = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.creator:
            return f"{self.creator.name} - {self.id}"
        return self.id

    @property
    def public_video_url(self):
        cache_key = f"ugc_public_video_url_{self.id}"
        url = cache.get(cache_key)

        if url is None:
            if not self.video:
                return None

            url = self.video.url
            cache.set(cache_key, url, settings.DEFAULT_STORAGE_QUERYSTRING_EXPIRE)

        return url

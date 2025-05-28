from django.db import models

from booth.models import Creator
from shortid import shortid


class Ugc(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=6,
        default=shortid,
        editable=False,
    )
    creator = models.ForeignKey(Creator, null=True, on_delete=models.SET_NULL)
    script = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.creator.name} - {self.id}"

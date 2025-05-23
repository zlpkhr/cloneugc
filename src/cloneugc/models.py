from django.db import models

from cloneugc.utils import shortid


class Actor(models.Model):
    id = models.CharField(
        primary_key=True, max_length=6, default=shortid, editable=False
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

from django.db import models
from lib.shortid import shortid


class Contact(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=6,
        default=shortid,
        editable=False,
    )
    name = models.TextField()
    email = models.EmailField()
    app_details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

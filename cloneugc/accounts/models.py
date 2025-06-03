from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from shortid import shortid


class Account(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=6,
        default=shortid,
        editable=False,
    )
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        editable=False,
    )
    credits = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.user.username

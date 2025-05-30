from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator


class Account(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        editable=False,
    )
    credits = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.user.username

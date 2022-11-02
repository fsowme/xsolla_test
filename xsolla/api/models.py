from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models


class Pay(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_id = models.IntegerField()
    canceled = models.BooleanField(default=False)


class User(AbstractUser):
    country = models.CharField(blank=True, max_length=2, validators=[MinLengthValidator(2)])
    player_id = models.CharField(max_length=255)

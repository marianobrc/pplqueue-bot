from django.db import models
from django.contrib.auth.models import AbstractUser
from model_utils.models import UUIDModel


class CustomUser(UUIDModel, AbstractUser):
    # Map the users with Slack users
    slack_user_id = models.CharField(db_index=True, unique=True, max_length=255)

    class Meta:
        abstract = False
        app_label = 'accounts'
        ordering = ['-date_joined']

from django.db import models
from django.contrib.auth import get_user_model
from model_utils.models import UUIDModel, TimeStampedModel, SoftDeletableModel


class SlackChannel(UUIDModel, TimeStampedModel, SoftDeletableModel):
    channel_id = models.CharField(db_index=True, max_length=255)

    class Meta:
        abstract = False
        app_label = 'slack_messages'
        ordering = ['-created']


class MessageLink(UUIDModel, TimeStampedModel, SoftDeletableModel):


    class Priority(models.IntegerChoices):
        HIGHEST = 0
        HIGH = 1
        MEDIUM = 2
        LOW = 3
        LOWEST = 4

    # The channel the message belongs to
    channel = models.ForeignKey(
        SlackChannel,
        related_name="saved_messages_by_channel",
        on_delete=models.CASCADE
    )
    # This is a timestamp that is unique per channel
    ts = models.CharField(db_index=True, max_length=255)
    permalink = models.URLField()
    priority = models.PositiveSmallIntegerField(
        db_index=True,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    saved_by = models.ForeignKey(
        get_user_model(),
        related_name="saved_messages_by_user",
        on_delete=models.CASCADE
    )


    class Meta:
        abstract = False
        app_label = 'slack_messages'
        ordering = ['-created']

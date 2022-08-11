import time
import uuid
import pytest
from ..models import MessageLink
from .test_channels import create_channel
from accounts.tests.test_users import create_user, test_password


@pytest.fixture
def create_message(db, create_channel, create_user):

    def make_message(**kwargs):
        if 'channel' not in kwargs:
            kwargs['channel'] = create_channel()
        if 'ts' not in kwargs:
            kwargs['ts'] = str(round(time.time() * 1000))
        if 'permalink' not in kwargs:
            kwargs['permalink'] = f"https://test-link-{kwargs['ts']}"
        if 'saved_by' not in kwargs:
            kwargs['saved_by'] = create_user()
        return MessageLink.objects.create(**kwargs)
    return make_message


@pytest.mark.django_db
def test_message_create_minimal(create_channel, create_user):
    user = create_user()
    channel = create_channel()
    message_ts = "123456789"
    url = "https://some-link"
    MessageLink.objects.create(
        channel=channel,
        ts=message_ts,
        permalink=url,
        saved_by=user
    )
    msg_from_db = MessageLink.objects.get(channel=channel, ts=message_ts)
    assert msg_from_db.permalink == url
    assert msg_from_db.saved_by == user


@pytest.mark.django_db
def test_message_retrieve_by_id(create_message):
    msg = create_message(priority=MessageLink.Priority.LOW)
    msg_from_db = MessageLink.objects.get(id=msg.id)
    assert msg_from_db.id == msg.id
    assert msg_from_db.priority == MessageLink.Priority.LOW


@pytest.mark.django_db
def test_message_retrieve_by_channel_and_ts(create_message):
    msg = create_message(priority=MessageLink.Priority.LOW)
    msg_from_db = MessageLink.objects.get(channel=msg.channel, ts=msg.ts)
    assert msg_from_db.priority == MessageLink.Priority.LOW


@pytest.mark.django_db
def test_message_update(create_message):
    msg = create_message(priority=MessageLink.Priority.MEDIUM)
    msg.priority = MessageLink.Priority.HIGHEST
    msg.save()
    msg.refresh_from_db()
    assert msg.priority == MessageLink.Priority.HIGHEST


@pytest.mark.django_db
def test_message_delete(create_message):
    msg = create_message()
    MessageLink.objects.get(id=msg.id).delete()
    assert not MessageLink.objects.filter(id=msg.id).exists()

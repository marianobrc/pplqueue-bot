import uuid

import pytest
from ..models import SlackChannel


@pytest.fixture
def create_channel(db):

    def make_channel(**kwargs):
        if 'channel_id' not in kwargs:
            kwargs['channel_id'] = str(uuid.uuid4())[:8]
        return SlackChannel.objects.create(**kwargs)
    return make_channel


@pytest.mark.django_db
def test_channel_create():
    channel_id = "ABCD12345"
    SlackChannel.objects.create(channel_id=channel_id)
    assert SlackChannel.objects.count() == 1
    channel = SlackChannel.objects.get(channel_id=channel_id)
    assert channel.channel_id == channel_id


@pytest.mark.django_db
def test_channel_retrieve(create_channel):
    new_channel = create_channel()
    channel_from_db = SlackChannel.objects.get(id=new_channel.id)
    assert channel_from_db.id == new_channel.id


@pytest.mark.django_db
def test_channel_retrieve_by_slack_id(create_channel):
    slack_id = "SOMEID123"
    create_channel(channel_id=slack_id)
    channel_from_db = SlackChannel.objects.get(channel_id=slack_id)
    assert channel_from_db.channel_id == slack_id


@pytest.mark.django_db
def test_channel_update_slack_id(create_channel):
    new_slack_id = "NEWID1234"
    new_channel = create_channel()
    new_channel.channel_id = new_slack_id
    new_channel.save()
    new_channel.refresh_from_db()
    assert new_channel.channel_id == new_slack_id


@pytest.mark.django_db
def test_channel_delete(create_channel):
    slack_id = "SOMEID123"
    create_channel(channel_id=slack_id)
    SlackChannel.objects.get(channel_id=slack_id).delete()
    assert not SlackChannel.objects.filter(channel_id=slack_id).exists()

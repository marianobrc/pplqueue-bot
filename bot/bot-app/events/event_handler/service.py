from slack_messages.models import SlackChannel, MessageLink
from django.contrib.auth import get_user_model
from .handlers import app_mention
from .errors import UnknownEvent


# Add new event handlers on this file
event_handlers = {
    'app_mention': app_mention,
}


def handle_event(slack_event):
    if "event" in slack_event:
        # Keep track of the existent channels and Users in the DB
        channel_id = slack_event['event']['channel']
        user_id = slack_event['event']['user'].strip()
        channel, _ = SlackChannel.objects.get_or_create(channel_id=channel_id)
        user, created =  get_user_model().objects.get_or_create(slack_user_id=user_id)
        # Process events by type
        event_type = slack_event['event']['type']
        try:
            print(f'PROCESSING EVENT OF TYPE {event_type}, user: {user}')
            event_handlers[event_type](slack_event)
        except IndexError:
            raise UnknownEvent(f"Unknown event of type {event_type}")

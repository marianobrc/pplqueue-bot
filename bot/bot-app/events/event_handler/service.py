from .handlers import app_mention
from .errors import UnknownEvent


# Add new event handlers on this file
event_handlers = {
    'app_mention': app_mention,
}


def handle_event(slack_event):
    event_type = slack_event['event']['type']
    try:
        print(f'PROCESSING EVENT OF TYPE {event_type} ')
        event_handlers[event_type](slack_event)
    except IndexError:
        raise UnknownEvent(f"Unknown event of type {event_type}")

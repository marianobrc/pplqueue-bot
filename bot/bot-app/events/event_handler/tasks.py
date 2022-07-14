from celery import shared_task
from .service import handle_event


# A wrapper to run the event handler in a decoupled mode
@shared_task
def event_handler_task(slack_event):
    handle_event(slack_event)


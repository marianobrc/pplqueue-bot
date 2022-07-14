import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from slack_sdk.signature import SignatureVerifier
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


slack_client = WebClient(token=settings.SLACK_BOT_TOKEN)
logger = logging.getLogger(__name__)


def verify_signed_request(request):
    verifier = SignatureVerifier(signing_secret=settings.SLACK_SIGNING_SECRET)
    timestamp = request.headers.get("x-slack-request-timestamp")
    signature = request.headers.get("x-slack-signature")
    body = request.body  # Raw payload
    return verifier.is_valid(body, timestamp, signature)


# Solves the slack challenge required to verity the url where events are sent
def url_verification(slack_event):
    return Response(
        data=slack_event['challenge'],
        status=status.HTTP_200_OK
    )


def app_mention(slack_event):
    # Get the channel to respond to
    channel_id = slack_event['event']['channel']
    user_id = slack_event['event']['user']
    print(f'[app_mention]> Got a message from channel {channel_id}, user {user_id}')
    send_greetings(channel_id, user_id)


def send_greetings(channel_id, user_id):
    try:
        # Say hi to the user that has mentioned me
        greeting_msg = f"Hi <@{user_id}> :wave: How can I help?"
        if user_id == "U03P0TM43SA":
            greeting_msg = f"Hi <@{user_id}> :heart_eyes:  Ask me anything!"
        print(f'Answering:\n{greeting_msg}')
        result = slack_client.chat_postMessage(
            channel=channel_id,
            text=greeting_msg
            # You could also use a blocks[] array to send richer content
        )
        # Print result, which includes information about the message (like TS)
        print(f'Slack API answer: {result}')

    except SlackApiError as e:
        print(f"Error: {e}")


event_handlers = {
    'url_verification': url_verification,
    'app_mention': app_mention,
}


def get_event_type(slack_event):
    event_type = slack_event.get('type')
    if event_type == 'event_callback':
        event_type = slack_event['event']['type']
    return event_type


class EventsAPIView(APIView):

    def post(self, request, *args, **kwargs):
        # Verify the request
        if not verify_signed_request(request):
            # For debugging only
            print(f'RECEIVED A REQUEST WITH AN INVALID SIGNATURE:\n{request}')
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # Parse the event
        slack_event = request.data
        # Choose the right handler depending on the event type
        event_type = get_event_type(slack_event)
        # For debugging only
        print(f'EVENT RECEIVED of type {event_type}: \n{slack_event}')
        # ToDo: Handle events in background
        if event_type in event_handlers:
            handler_response = event_handlers[event_type](slack_event)
            # Some events might require a custom response
            if handler_response:
                return handler_response
        else:
            print(f'UNKNOWN EVENT with type `{event_type}`')

        # In general, respond with a generic success status
        return Response(status=status.HTTP_200_OK)

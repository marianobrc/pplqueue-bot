import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from slack_sdk.signature import SignatureVerifier
from .event_handler.tasks import event_handler_task


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


class EventsAPIView(APIView):

    def post(self, request, *args, **kwargs):
        # Verify the request
        if not verify_signed_request(request):
            # For debugging only
            print(f'RECEIVED A REQUEST WITH AN INVALID SIGNATURE:\n{request}')
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # Parse the event
        slack_event = request.data
        # For debugging only
        print(f'EVENT RECEIVED of type {slack_event.get("type")}: \n{slack_event}')
        # Respond to the url verification challenge
        if slack_event.get('type') == 'url_verification':
            return url_verification(slack_event)

        # Process the event in background
        event_handler_task.delay(slack_event)

        # In general, respond with a generic success status
        return Response(status=status.HTTP_200_OK)

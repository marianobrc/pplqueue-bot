import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from slack_sdk.signature import SignatureVerifier


# Get an instance of a logger
logger = logging.getLogger(__name__)


def verify_signed_request(request):
    verifier = SignatureVerifier(signing_secret=settings.SLACK_SIGNING_SECRET)
    timestamp = request.headers.get("x-slack-request-timestamp")
    signature = request.headers.get("x-slack-signature")
    body = request.body  # Raw payload
    return verifier.is_valid(body, timestamp, signature)


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
        print(f'EVENT RECEIVED:\n{slack_event}')

        # Respond to the verification challenge
        event_type = slack_event.get('type')
        if event_type == 'url_verification':
            return Response(
                data=slack_event['challenge'],
                status=status.HTTP_200_OK
            )

        # ToDo: Handle other events
        return Response(status=status.HTTP_200_OK)

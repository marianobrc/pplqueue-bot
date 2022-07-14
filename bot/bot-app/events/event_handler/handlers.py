import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from django.conf import settings


logger = logging.getLogger(__name__)
slack_client = WebClient(token=settings.SLACK_BOT_TOKEN)


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

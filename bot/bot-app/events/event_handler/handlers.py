import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from django.conf import settings
from django.contrib.auth import get_user_model
from slack_messages.models import SlackChannel, MessageLink
from .errors import LinkGenerationError


logger = logging.getLogger(__name__)
slack_client = WebClient(token=settings.SLACK_BOT_TOKEN)


def app_mention(slack_event):
    # Get the channel to respond to
    channel_id = slack_event['event']['channel']
    user_id = slack_event['event']['user']
    text = slack_event['event']['text']
    print(f'[app_mention]> Got a message from channel {channel_id}, user {user_id}: \n {text}')

    # Parse commands
    # "save message"
    if "save" in text and "message" in text:
        # ToDo: Parse priority from the text
        save_message(slack_event)
    elif "list" in text:  # Retrieve message list
        list_messages(slack_event)
    else:  # Default response if no other command is recognized
        send_greetings(slack_event)


def save_message(slack_event, priority=MessageLink.Priority.MEDIUM):
    # Check if there is a message in a thread
    if "thread_ts" not in slack_event['event']:
        send_save_message_help(slack_event)
        return
    # Save a link to the thread
    channel_id = slack_event['event']['channel']
    message_id = slack_event['event']['thread_ts']
    user_id = slack_event['event']['user'].strip()
    try:
        permalink = get_message_permalink(channel_id, message_id)
    except LinkGenerationError:
        send_error_message(slack_event, error_details="I couldn't save your message")
        return
    print(f"[save_message]> Link: {permalink}")
    # Save the message, only once
    channel = SlackChannel.objects.get(channel_id=channel_id)  # FixMe: Could we get more than one?
    user = get_user_model().objects.get(slack_user_id=user_id)
    MessageLink.objects.get_or_create(
        channel=channel,
        ts=message_id,
        defaults = {
            "permalink": permalink,
            "saved_by": user,
            "priority": priority
        }
    )
    # Confirm the message was saved
    send_message_saved(slack_event)


def list_messages(slack_event):
    # Get the saved messages ordered by priority and then by timestamp
    user_id = slack_event['event']['user'].strip()
    user = get_user_model().objects.get(slack_user_id=user_id)
    messages = MessageLink.objects.filter(saved_by=user, is_removed=False).order_by('priority', 'created')
    # Build a list to show in slack
    messages_list_str = "These are your saved messages:"+ "".join(
        [f"\n\t * {message.permalink}" for message in messages]
    )
    send_text_response_to_slack(slack_event, messages_list_str)


def get_message_permalink(channel_id, message_id):
    try:
        print(f'Getting permalink to message: {message_id}')
        result = slack_client.chat_getPermalink(
            channel=channel_id,
            message_ts=message_id
        )
        # Print result, which includes information about the message (like TS)
        print(f'Slack API answer: {result}')
    except SlackApiError as e:
        print(f"Error: {e}")
    else:
        if not result['ok']:
            raise LinkGenerationError
        # {'ok': True, 'permalink': 'https://pplqueueworkspace.slack.com/archives/C03P7FRBN6N/p1657826870783359?thread_ts=1657826870.783359&cid=C03P7FRBN6N', 'channel': 'C03P7FRBN6N'}
        return result['permalink']


# Helper functions to send messages to slack


def send_text_response_to_slack(slack_event, response_text):
    try:
        channel_id = slack_event['event']['channel']
        user_id = slack_event['event']['user']
        answer = f"<@{user_id}> {response_text}"
        print(f'Answering:\n{answer}')
        if "thread_ts" in slack_event['event']:  # Respond in the same Thread
            result = slack_client.chat_postMessage(
                channel=channel_id,
                thread_ts=slack_event['event']['thread_ts'],
                text=answer
                # You could also use a blocks[] array to send richer content
            )
        else:  # Respond in the channel
            result = slack_client.chat_postMessage(
                channel=channel_id,
                text=answer
                # You could also use a blocks[] array to send richer content
            )
        # Print result, which includes information about the message (like TS)
        print(f'Slack API answer: {result}')

    except SlackApiError as e:
        print(f"Error: {e}")


def send_save_message_help(slack_event):
    send_text_response_to_slack(
        slack_event=slack_event,
        response_text="please use this command as a threaded message in the message you want to save"
    )


def send_message_saved(slack_event):
    send_text_response_to_slack(
        slack_event=slack_event,
        response_text="your message was saved!"
    )


def send_error_message(slack_event, error_details=""):
    send_text_response_to_slack(
        slack_event=slack_event,
        response_text=f"Oops! {error_details or 'Something went wrong' }. Try again later."
    )


def send_greetings(slack_event):
    send_text_response_to_slack(
        slack_event=slack_event,
        response_text=":wave: How can I help?"
    )

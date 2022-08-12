import pytest
from django.urls import reverse
from django.conf import settings
from rest_framework import status
from slack_sdk.signature import SignatureVerifier
from ..models import MessageLink


@pytest.mark.django_db
def test_url_verification(signed_api_client):
    verification_data = {
        "token": "SoMeTok3nN0tR34llyUsed",
        "challenge": "Nf8QRlbM6MNpCrwP6XaGyuXKdRmnZbxVrW36JOc8Wqaeo2hPJAEP",
        "type": "url_verification",
    }
    signer = SignatureVerifier(signing_secret=settings.SLACK_SIGNING_SECRET)
    events_url = reverse("slack-events")
    response = signed_api_client.signed_post(
        events_url, data=verification_data, signer=signer, format="json"
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_event__app_mention__send_greetings(signed_api_client, mocker, slack_event_empty_mention):
    event_data = slack_event_empty_mention
    # Mock out requests to slack api
    mock_obj = mocker.patch(
        "slack_messages.event_handlers.handlers.send_text_response_to_slack",
    )
    # The requests must be signed
    signer = SignatureVerifier(signing_secret=settings.SLACK_SIGNING_SECRET)
    events_url = reverse("slack-events")
    response = signed_api_client.signed_post(
        events_url, data=event_data, signer=signer, format="json"
    )
    assert response.status_code == status.HTTP_200_OK
    # Check that the roper response msg was sent to slack
    _, kwargs = mock_obj.call_args_list[-1]
    assert mock_obj.call_count == 1
    assert kwargs["slack_event"] == event_data
    assert kwargs["response_text"] == ":wave: How can I help?"


@pytest.mark.django_db
def test_event__app_mention__save_message(signed_api_client, mocker, slack_event_save_message):
    event_data = slack_event_save_message
    # Mock out requests to slack api
    mock_msg_to_slack = mocker.patch(
        "slack_messages.event_handlers.handlers.send_text_response_to_slack",
    )
    # Mock the permalink generation
    fake_permalink = "https://myworkspace.slack.com/archives/CHAN7FRBN6N/p1657826870783359?thread_ts=1660312937.906649&cid=CHAN7FRBN6N"
    mock_permalink = mocker.patch(
        "slack_messages.event_handlers.handlers.get_message_permalink",
        return_value=fake_permalink
    )
    # The requests must be signed
    signer = SignatureVerifier(signing_secret=settings.SLACK_SIGNING_SECRET)
    events_url = reverse("slack-events")
    response = signed_api_client.signed_post(
        events_url, data=event_data, signer=signer, format="json"
    )
    # Check the API response
    assert response.status_code == status.HTTP_200_OK
    # Check that a MessageLink was created in the database
    msg_link = MessageLink.objects.get(
        saved_by__slack_user_id=event_data['event']['user'],
        channel__channel_id=event_data['event']['channel'],
        ts=event_data['event']['thread_ts'],  # The id of the parent msg or thread
    )
    assert msg_link.permalink == fake_permalink
    assert msg_link.priority == MessageLink.Priority.MEDIUM  # default
    # Check that the proper response msg was sent to slack
    _, kwargs = mock_msg_to_slack.call_args_list[-1]
    assert mock_msg_to_slack.call_count == 1
    assert kwargs["slack_event"] == event_data
    assert kwargs["response_text"] == "your message was saved!"


@pytest.mark.django_db
def test_event__app_mention__save_message_two_users(signed_api_client, mocker, slack_event_save_message):
    event_data_user_1 = slack_event_save_message
    event_data_user_1['event']['user'] = "USER1111111"
    event_data_user_2 = slack_event_save_message
    event_data_user_2['event']['user'] = "USER2222222"

    # Mock out requests to slack api
    mock_msg_to_slack = mocker.patch(
        "slack_messages.event_handlers.handlers.send_text_response_to_slack",
    )
    # Mock the permalink generation
    fake_permalink = "https://myworkspace.slack.com/archives/CHAN7FRBN6N/p1657826870783359?thread_ts=1660312937.906649&cid=CHAN7FRBN6N"
    mock_permalink = mocker.patch(
        "slack_messages.event_handlers.handlers.get_message_permalink",
        return_value=fake_permalink
    )
    # The requests must be signed
    signer = SignatureVerifier(signing_secret=settings.SLACK_SIGNING_SECRET)
    events_url = reverse("slack-events")

    # Save message using user 1
    response = signed_api_client.signed_post(
        events_url, data=event_data_user_1, signer=signer, format="json"
    )
    # Check the API response
    assert response.status_code == status.HTTP_200_OK
    # Check that a MessageLink was created in the database
    assert MessageLink.objects.count() == 1
    msg_link = MessageLink.objects.get(
        saved_by__slack_user_id=event_data_user_1['event']['user'],
        channel__channel_id=event_data_user_1['event']['channel'],
        ts=event_data_user_1['event']['thread_ts'],  # The id of the parent msg or thread
    )
    assert msg_link.permalink == fake_permalink
    assert msg_link.priority == MessageLink.Priority.MEDIUM  # default
    # Check that the proper response msg was sent to slack
    _, kwargs = mock_msg_to_slack.call_args_list[-1]
    assert mock_msg_to_slack.call_count == 1
    assert kwargs["slack_event"] == event_data_user_1
    assert kwargs["response_text"] == "your message was saved!"

    # Now save the same message using user 2
    response = signed_api_client.signed_post(
        events_url, data=event_data_user_2, signer=signer, format="json"
    )
    # Check the API response
    assert response.status_code == status.HTTP_200_OK
    # Check that a MessageLink was created in the database
    assert MessageLink.objects.count() == 2
    msg_link = MessageLink.objects.get(
        saved_by__slack_user_id=event_data_user_2['event']['user'],
        channel__channel_id=event_data_user_2['event']['channel'],
        ts=event_data_user_2['event']['thread_ts'],  # The id of the parent msg or thread
    )
    assert msg_link.permalink == fake_permalink
    assert msg_link.priority == MessageLink.Priority.MEDIUM  # default
    # Check that the proper response msg was sent to slack
    _, kwargs = mock_msg_to_slack.call_args_list[-1]
    assert mock_msg_to_slack.call_count == 2
    assert kwargs["slack_event"] == event_data_user_2
    assert kwargs["response_text"] == "your message was saved!"

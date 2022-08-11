import pytest
from django.urls import reverse
from django.conf import settings
from rest_framework import status
from slack_sdk.signature import SignatureVerifier


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
def test_event_app_mention__request(signed_api_client):
    event_data = {
        "token": "SoMeTok3nN0tR34llyUsed",
        "team_id": "TEAMX8M7UCQ",
        "api_app_id": "APPIDGMQSFD2",
        "event": {
            "client_msg_id": "e2aed917-d68d-45c4-9c27-920afce3cfb0",
            "type": "app_mention",
            "text": "hi <@USER2P55TQF>",
            "user": "USER7FVUQHG",
            "ts": "1660260792.551909",
            "team": "TEAMX8M7UCQ",
            "blocks": [
                {
                    "type": "rich_text",
                    "block_id": "c/p",
                    "elements": [
                        {
                            "type": "rich_text_section",
                            "elements": [
                                {"type": "text", "text": "hi "},
                                {"type": "user", "user_id": "USER2P55TQF"},
                            ],
                        }
                    ],
                }
            ],
            "channel": "CHAN7FRBN6N",
            "event_ts": "1660260792.551909",
        },
        "type": "event_callback",
        "event_id": "Ev03T6EG7C2J",
        "event_time": 1660260792,
        "authorizations": [
            {
                "enterprise_id": None,
                "team_id": "TEAMX8M7UCQ",
                "user_id": "USER7FVUQHG",
                "is_bot": True,
                "is_enterprise_install": False,
            }
        ],
        "is_ext_shared_channel": False,
        "event_context": "4-eyJldCI6ImFwcF9tZW50aW9uIiwidGlkIjoiVDAzUFg4TTdVQ1EiLCJhaWQiOiJBMDNQR01RU0ZEMiIsImNpZCI6IkMwM1A3RlJCTjZOIn0",
    }
    signer = SignatureVerifier(signing_secret=settings.SLACK_SIGNING_SECRET)
    events_url = reverse("slack-events")
    response = signed_api_client.signed_post(
        events_url, data=event_data, signer=signer, format="json"
    )
    #ToDo: Mock/Stub the send_text_response_to_slack method
    assert response.status_code == status.HTTP_200_OK

import pytest
from rest_framework.test import APIClient


class SignedAPIClient(APIClient):

    def signed_post(self, path, signer, data=None, format=None, content_type=None,
                    follow=False, **extra):
        data, content_type = self._encode_data(data, format, content_type)
        timestamp = signer.clock.now()
        signature = signer.generate_signature(
            timestamp=timestamp,
            body=data
        )
        extra['HTTP_X_SLACK_REQUEST_TIMESTAMP'] = timestamp
        extra['HTTP_X_SLACK_SIGNATURE'] = signature
        response = super().generic('POST', path, data, content_type, **extra)
        if follow:
            response = self._handle_redirects(response, **extra)
        return response


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def signed_api_client():
    return SignedAPIClient()


@pytest.fixture
def slack_event_empty_mention():
    def make_event():
        return {
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
    return make_event


@pytest.fixture
def slack_event_save_message():

    def make_event():
        return {
            "token": "SoMeTok3nN0tR34llyUsed",
            "team_id": "TEAMX8M7UCQ",
            "api_app_id": "APPIDGMQSFD2",
            "event": {
                "client_msg_id": "6c625b0e-bd46-420c-9afd-813b6e8ce638",
                "type": "app_mention",
                "text": "<@USER2P55TQF> save",
                "user": "USER2P55TQF",
                "ts": "1660312949.047499",
                "team": "TEAMX8M7UCQ",
                "blocks": [
                    {
                        "type": "rich_text",
                        "block_id": "fGP",
                        "elements": [
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {"type": "user", "user_id": "USER2P55TQF"},
                                    {"type": "text", "text": " save"},
                                ],
                            }
                        ],
                    }
                ],
                "thread_ts": "1660312937.906649",
                "parent_user_id": "USER2P55TQF",
                "channel": "CHAN7FRBN6N",
                "event_ts": "1660312949.047499",
            },
            "type": "event_callback",
            "event_id": "Ev03U5D4GG56",
            "event_time": 1660312949,
            "authorizations": [
                {
                    "enterprise_id": None,
                    "team_id": "TEAMX8M7UCQ",
                    "user_id": "USER2P55TQF",
                    "is_bot": True,
                    "is_enterprise_install": False,
                }
            ],
            "is_ext_shared_channel": False,
            "event_context": "4-eyJldCI6ImFwcF9tZW50aW9uIiwidGlkIjoiVDAzUFg4TTdVQ1EiLCJhaWQiOiJBMDNQR01RU0ZEMiIsImNpZCI6IkMwM1A3RlJCTjZOIn0",
        }
    return make_event

import json

import pytest
from django.urls import reverse
from django.conf import settings
from rest_framework import status
from slack_sdk.signature import SignatureVerifier

@pytest.mark.django_db
def test_url_verification(signed_api_client):
    verification_data = {
        'token': 'SoMeTok3nN0tR34llyUsed',
        'challenge': 'Nf8QRlbM6MNpCrwP6XaGyuXKdRmnZbxVrW36JOc8Wqaeo2hPJAEP',
        'type': 'url_verification'
    }
    signer = SignatureVerifier(signing_secret=settings.SLACK_SIGNING_SECRET)
    events_url = reverse('slack-events')
    response = signed_api_client.signed_post(
        events_url,
        data=verification_data,
        signer=signer,
        format='json'
    )
    assert response.status_code == status.HTTP_200_OK

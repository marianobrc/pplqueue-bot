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

import pytest
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def test_password():
    return 'strong-test-pass'


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        if 'slack_user_id' not in kwargs:
            kwargs['slack_user_id'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.mark.django_db
def test_user_create():
    User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword', slack_user_id="my-slack-user-id")
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_user_retrieve_by_slack_id(create_user):
    slack_user_id = "ABCD123"
    create_user(slack_user_id=slack_user_id)
    user = User.objects.get(slack_user_id=slack_user_id)
    assert user.slack_user_id == slack_user_id


@pytest.mark.django_db
def test_user_update_email(create_user):
    new_email = "email@changed.com"
    slack_user_id = "ABCD123"
    create_user(slack_user_id=slack_user_id)
    user = User.objects.get(slack_user_id=slack_user_id)
    user.email = new_email
    user.save()
    user.refresh_from_db()
    assert user.email == new_email


@pytest.mark.django_db
def test_user_delete(create_user):
    slack_user_id = "ABCD123"
    create_user(slack_user_id=slack_user_id)
    User.objects.filter(slack_user_id=slack_user_id).delete()
    assert not User.objects.filter(slack_user_id=slack_user_id).exists()

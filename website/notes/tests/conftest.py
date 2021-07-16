import pytest
from django.contrib.auth.models import User

from ..models import Note


@pytest.fixture
def current_user(client):
    """Register a new user and authenticate as them."""
    user = User.objects.create_user(
        username='test', password='extremelypinkrose'
    )
    client.force_login(user)
    return user


@pytest.fixture
def other_user():
    """Register a new user, but don't authenticate as them."""
    return User.objects.create_user(username='other', password='thisisnotrelavant')


@pytest.fixture
def note1(current_user):
    return Note.objects.create(author=current_user, title='Example note 1')


@pytest.fixture
def note2(current_user):
    return Note.objects.create(author=current_user, title='Example note 2')


@pytest.fixture
def other_note(other_user):
    return Note.objects.create(author=other_user, title='Example note')

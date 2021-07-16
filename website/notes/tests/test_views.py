import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_index(client):
    response = client.get(reverse('notes:index'))
    assert response.status_code == 200
    assert response.context['title'] == 'Public Notes'


@pytest.mark.django_db
def test_my(client):
    response = client.get(reverse('notes:my'))
    assert response.status_code == 200
    assert response.context['title'] == 'My Notes'

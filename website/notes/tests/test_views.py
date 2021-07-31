import pytest
from django.urls import reverse

from ..models import Note
from ..forms import CreateCommentForm


@pytest.mark.django_db
def test_index(client):
    response = client.get(reverse('notes:index'))
    assert response.status_code == 200
    assert response.context['title'] == 'All Notes'


@pytest.mark.django_db
def test_my(client):
    response = client.get(reverse('notes:my'))
    assert response.status_code == 200
    assert response.context['title'] == 'My Notes'


@pytest.mark.django_db
class TestRead:

    def test_unauthenticated_user(self, client, note1):
        client.logout()
        response = client.get(
            reverse('notes:read', kwargs={'note_id': note1.uuid}))
        assert 300 <= response.status_code < 400
        assert response.context is None

    def test_existent_note(self, client, current_user, note1):
        response = client.get(
            reverse('notes:read', kwargs={'note_id': note1.uuid}))
        assert response.status_code == 200
        assert response.context['title'] == note1.title
        assert response.context['note'] == note1
        assert isinstance(response.context['create_comment_form'], CreateCommentForm)  # noqa
        # TODO: test if the categories are properly selected

    def test_nonexistent_note(self, client, current_user):
        response = client.get(reverse('notes:read', kwargs={
                              'note_id': 'b5ba9036-4cda-4aa4-8b49-9e0ca1fba6a1'}))
        assert response.status_code == 404

    def test_foreign_note(self, client, current_user, other_note):
        response = client.get(
            reverse('notes:read', kwargs={'note_id': other_note.uuid}))
        assert response.status_code == 404


@pytest.mark.django_db
class TestEdit:

    def test_unauthenticated_user(self, client, note1):
        client.logout()
        response = client.get(
            reverse('notes:edit', kwargs={'note_id': note1.uuid}))
        assert 300 <= response.status_code < 400
        assert response.context is None

    def test_existent_note(self, client, note1):
        response = client.get(
            reverse('notes:edit', kwargs={'note_id': note1.uuid}))
        assert response.status_code == 200
        assert response.context['title'] == note1.title
        assert response.context['note'] == note1

    def test_nonexistent_note(self, client, current_user):
        response = client.get(reverse('notes:edit', kwargs={
                              'note_id': 'b5ba9036-4cda-4aa4-8b49-9e0ca1fba6a1'}))
        assert response.status_code == 404

    def test_foreign_note(self, client, current_user, other_note):
        response = client.get(
            reverse('notes:edit', kwargs={'note_id': other_note.uuid}))
        assert response.status_code == 404

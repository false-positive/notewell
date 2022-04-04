"""Render input data for editor."""

from django import template
from django.utils.safestring import mark_safe
from rest_framework.renderers import JSONRenderer

from notes.serializers import NoteSerializer

register = template.Library()


@register.simple_tag
def render_initial_editor_data(*, note, token_pair, open_dialog):
    # XXX: may be unsafe ?
    return mark_safe(JSONRenderer().render({
        'note': NoteSerializer(note).data,
        'definitely_not_token_pair': token_pair,
        'open_dialog': open_dialog,
    }).decode('utf-8'))

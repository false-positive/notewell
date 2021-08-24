"""Render input data for editor."""

import json

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def render_initial_editor_data(*, note, token_pair):
    # XXX: may be unsafe ?
    return mark_safe(json.dumps({
        # 'note': {
        #     'author': note.author.username,
        #     'uuid': note.uuid,
        #     'title': note.title,
        #     'date_created': note.date_created,
        #     'categories': []
        # },
        'definitely_not_token_pair': token_pair,
        'note': {'uuid': str(note.uuid)},
    }, separators=(',', ':')))

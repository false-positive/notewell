from django.shortcuts import get_object_or_404

from .models import Note


def get_accessible_note_or_404(user_pk, klass=Note, *args, **kwargs):
    if klass is Note:
        klass = Note.objects

    klass = klass.filter_accessible_notes_by(user_pk)

    return get_object_or_404(klass, *args, **kwargs)

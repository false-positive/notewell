from math import ceil
from itertools import chain

from django.shortcuts import get_object_or_404, render

from .models import Note, Category


def get_accessible_note_or_404(user_pk, klass=Note, *args, **kwargs):
    if klass is Note:
        klass = Note.objects

    klass = klass.filter_accessible_notes_by(user_pk)

    return get_object_or_404(klass, *args, **kwargs)


def search(request, search_query):
    user = request.user
    notes_by_title = Note.objects.filter(title__icontains=search_query).filter_accessible_notes_by(user_pk=user.pk)
    notes_by_author = Note.objects.filter(author__username__icontains=search_query).filter_accessible_notes_by(user_pk=user.pk)

    notes = set(chain(notes_by_title, notes_by_author))

    return render(request, 'notes/note_list.html', {
        'title': f'Search results for "{search_query}"',
        'categories': Category.objects.all(),
        'object_list': notes,
    })


def get_notes(request, category=None, user=None):

    # TODO maybe fix limit bug
    notes_on_page = int(request.GET.get('limit', 10))
    page_num = int(request.GET.get('p', 1))

    start = notes_on_page * (page_num - 1)
    end = notes_on_page * page_num

    if user:
        notes = Note.objects \
            .select_related('author') \
            .prefetch_related('categories')\
            .filter(
                author=user
            ) \
            .filter_accessible_notes_by(user_pk=request.user.pk) \
            .distinct()

    elif category:
        notes = Note.objects \
            .select_related('author') \
            .prefetch_related('categories')\
            .filter(
                categories__in=category.get_descendants(include_self=True)
            ) \
            .filter_accessible_notes_by(user_pk=request.user.pk) \
            .distinct()
    else:
        notes = Note.objects \
            .select_related('author') \
            .filter(status='public') \
            # .filter_accessible_notes_by(user_pk=request.user.pk)

    # TODO maybe find a better way to return the values

    return {
        "notes": notes[start:end],
        "page_count": ceil(notes.count() / notes_on_page),
        "current_page": page_num,
    }

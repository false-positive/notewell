from django.shortcuts import get_object_or_404
from notes.models import Category, Note

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CategorySerializer, NoteSerializer


@api_view(['GET'])
def view_notes(request, cat_path=None):
    # TODO select only public notes
    if cat_path:
        path_exists = False

        for path in Category.objects.values('full_path'):
            if path['full_path'] == cat_path:
                path_exists = True

        if not path_exists:
            return Response(
                {'message': 'No notes were found'},
                status=status.HTTP_404_NOT_FOUND
            )

        cat_slug = cat_path.split('/')[-1]
        category: Category = get_object_or_404(Category, slug=cat_slug)

        # TODO: figure out how to make a join or something here
        notes = []

        def get_all_child_notes(category):
            for note in Note.objects.select_related('author').prefetch_related('categories').filter(categories=category):
                notes.append(note)

            for cat in category.children.all():
                get_all_child_notes(cat)

        get_all_child_notes(category)

    else:
        notes = Note.objects.select_related(
            'author').prefetch_related('categories').all()

    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def view_note(request, note_id=None):
    # TODO check if note is public or private
    # and if private ask for username and password

    note: Note = get_object_or_404(Note, uuid=note_id)
    serializer = NoteSerializer(note)
    return Response(serializer.data)


@api_view(['GET'])
def view_categories(request, cat_path=None):
    if cat_path:
        path_exists = False

        for path in Category.objects.values('full_path'):
            if path['full_path'] == cat_path:
                path_exists = True

        if not path_exists:
            return Response(
                {'message': 'Category not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        cat_slug = cat_path.split('/')[-1]
        categories = Category.objects \
            .prefetch_related('children' + '__children' * 5) \
            .filter(slug=cat_slug)
    else:
        categories = Category.objects.prefetch_related(
            'children' + '__children' * 5).filter(parent__isnull=True)

    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

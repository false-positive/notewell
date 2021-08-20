from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http.response import Http404
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    CategorySerializer,
    NoteSerializer,
    ViewNoteSerializer,
    UserSerializer,
)
from notes.models import Category, Note
from notes.shortcuts import get_accessible_note_or_404


@api_view(['GET'])
# @permission_classes((IsAuthenticated,))
def view_notes(request, cat_path=None):
    # TODO select only public notes
    user = request.user

    if cat_path:
        try:
            category: Category = get_object_or_404(Category, full_path=cat_path)
        except Http404:
            return Response(
                {'detail': 'Category not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        notes = Note.objects \
            .select_related('author') \
            .prefetch_related('categories')\
            .filter(
                categories__in=category.get_descendants(include_self=True)
            ) \
            .filter_accessible_notes_by(user.pk) \
            .distinct()
    else:

        notes = Note.objects \
            .select_related('author') \
            .prefetch_related('categories') \
            .filter_accessible_notes_by(user.pk)

    serializer = ViewNoteSerializer(notes, many=True)
    return Response(serializer.data)


@api_view(['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes((IsAuthenticated,))
def note_crud(request, note_id=None):
    # crud = create, read, update, delete
    request = request._request

    if request.method == 'GET':
        return view_note(request, note_id)
    elif request.method == 'POST':
        return create_note(request)
    elif request.method == 'GET':
        return view_note(request, note_id)
    elif request.method == 'PUT' or request.method == 'PATCH':
        return update_note(request, note_id)
    elif request.method == 'DELETE':
        return delete_note(request, note_id)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def view_note(request, note_id):
    # TODO check if note is public or private
    # and if private ask for username and password

    user = request.user

    try:
        note = get_accessible_note_or_404(user.pk, uuid=note_id)
    except Http404:
        return Response(
            {"detail": "You do not have permission to view this note"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = ViewNoteSerializer(note)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_note(request):
    serializer = NoteSerializer(data=request.data)
    data = {}

    user = request.user

    # TODO maybe make category not optional or smth
    if serializer.is_valid():
        note = Note()
        note.title = serializer.validated_data['title']
        note.author = user
        note.save()
        if serializer.validated_data.get('categories'):
            note.categories.set(serializer.validated_data['categories'])

        data = ViewNoteSerializer(note).data
        data['detail'] = 'Note created successfully'
    else:
        data = serializer.errors

    return Response(data)


@api_view(['PUT', 'PATCH'])
@permission_classes((IsAuthenticated,))
def update_note(request, note_id):
    note = Note.objects.get(uuid=note_id)
    serializer = NoteSerializer(instance=note, data=request.data)
    data = {}

    user = request.user

    if user != note.author:
        return Response(
            {'detail': 'You do not have permissions to update this note'}
        )

    # TODO maybe make category not optional or smth
    if serializer.is_valid():
        note.title = serializer.validated_data['title']
        note.save()
        if serializer.validated_data.get('categories'):
            note.categories.set(serializer.validated_data['categories'])

        data = ViewNoteSerializer(note).data
        data['detail'] = 'Note updated successfully'
    else:
        data = serializer.errors

    return Response(data)


@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def delete_note(request, note_id):
    user = request.user
    note = Note.objects.get(uuid=note_id)
    data = {}

    if user == note.author:
        note.delete()
        data['detail'] = 'Note deleted successfully'
    else:
        data['detail'] = 'You do not have permissions to delete this note'

    return Response(data)


@api_view(['GET'])
def view_categories(request, cat_path=None):
    if cat_path:
        categories = Category.objects \
            .prefetch_related('children' + '__children' * 5) \
            .filter(full_path=cat_path)

        if not categories:
            return Response(
                {'detail': 'Category not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    else:
        categories = Category.objects.prefetch_related(
            'children' + '__children' * 5).filter(parent__isnull=True)

    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def view_users(request):
    users = User.objects.filter(is_active=True)

    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)

    data = {}
    if serializer.is_valid():
        serializer.validated_data['password'] = make_password(
            serializer.validated_data['password']
        )
        user = serializer.save()

        data['message'] = 'User registered successfully'
        data['email'] = user.email
        data['username'] = user.username
        data['token'] = Token.objects.get(user=user).key
    else:
        data = serializer.errors

    return Response(data)


@api_view(['GET'])
def test(request):

    serializer = CategorySerializer(Category.objects.prefetch_related(
        'children' + '__children' * 5).filter(parent__isnull=True), many=True)

    return Response(serializer.data)

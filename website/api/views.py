from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http.response import Http404
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import CategorySerializer, NoteSerializer, UserSerializer
from notes.models import Category, Note
from notes.shortcuts import get_accessible_note_or_404


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
            current_notes = Note.objects \
                .select_related('author') \
                .prefetch_related('categories') \
                .filter(categories=category)

            for note in current_notes:
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


@api_view(['GET'])
def view_users(request):
    users = User.objects.all()

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

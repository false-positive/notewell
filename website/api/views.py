from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    AuthUserSerializer,
    AuthUserTokenObtainPairSerializer,
    CategorySerializer,
    NoteSerializer,
    ViewNoteSerializer,
    UserSerializer,
)
from .shortcuts import generate_jwt_token
from notes.models import Category, Note
from notes.shortcuts import get_accessible_note_or_404


class NoteList(APIView):
    """List all notes, or create a new one."""

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        """List all notes accessible to user. Filter to category, if passed"""
        user = request.user

        cat_path = request.query_params.get('category')
        if cat_path:
            try:
                notes = self._get_notes_in_category(user, cat_path)
            except Http404:
                return Response(
                    {'detail': 'Category not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            notes = self._get_notes(user)

        serializer = ViewNoteSerializer(notes, many=True)
        return Response({'data': serializer.data})

    def post(self, request, format=None):
        """Create a new note."""
        serializer = NoteSerializer(data=request.data)

        user = request.user

        # TODO: maybe make category not optional or smth
        if serializer.is_valid():
            serializer.save(author=user)
            return Response(
                {'data': serializer.data, 'detail': 'Note created successfully'},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def _get_notes_in_category(self, user, cat_path):
        """Query all notes accessible by user in category at cat_path."""
        category: Category = get_object_or_404(Category, full_path=cat_path)

        return Note.objects \
            .select_related('author') \
            .prefetch_related('categories')\
            .filter(
                categories__in=category.get_descendants(include_self=True)
            ) \
            .filter_accessible_notes_by(user.pk) \
            .distinct()  # Q: why do we need distinct here?

    def _get_notes(self, user):
        """Query all notes accessible by user."""
        return Note.objects \
            .select_related('author') \
            .prefetch_related('categories') \
            .filter_accessible_notes_by(user.pk)


class NoteDetail(APIView):
    """Read, Patch or Delete Note."""

    def get(self, request, note_id, format=None):
        """Get note."""
        user = request.user

        try:
            note = get_accessible_note_or_404(user.pk, uuid=note_id)
        except Http404:
            return Response(
                {'detail': 'Note not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ViewNoteSerializer(note)
        return Response({'data': serializer.data})

    def patch(self, request, note_id, format=None):
        """Patch note."""
        user = request.user

        try:
            note = get_accessible_note_or_404(user.pk, uuid=note_id)
            if not note.can_be_edited_by(user):
                raise Http404()  # HACK: pretending as if lookup failed
        except Http404:
            return Response(
                {'detail': 'Note not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = NoteSerializer(instance=note, data=request.data)

        # TODO maybe make category not optional or smth
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data})
        return Response(
            {'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, note_id, format=None):
        """Delete note."""
        user = request.user

        try:
            note = get_accessible_note_or_404(user.pk, uuid=note_id)
            if not note.can_be_edited_by(user):
                raise Http404()  # HACK: pretending as if lookup failed
        except Http404:
            return Response(
                {'detail': 'Note not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



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
    return Response({'data': serializer.data})


@api_view(['GET'])
def view_users(request):
    users = User.objects.filter(is_active=True)

    serializer = UserSerializer(users, many=True)
    return Response({'data': serializer.data})


@api_view(['POST'])
def register(request):
    serializer = AuthUserSerializer(data=request.data)

    data = {}
    if serializer.is_valid():
        serializer.validated_data['password'] = make_password(
            serializer.validated_data['password']
        )
        user = serializer.save()

        data['detail'] = 'User registered successfully'
        data['email'] = user.email
        data['username'] = user.username
        # XXX only for python 3.5 or higher
        data = {**data, **generate_jwt_token(user)}
    else:
        data = serializer.errors

    return Response({'data': data})


class UserTokenPairView(TokenObtainPairView):
    serializer_class = AuthUserTokenObtainPairSerializer


class UserAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .ai import sum_text, gen_quest, text_subject, text_quality

from .serializers import (
    AuthUserSerializer,
    AuthUserTokenObtainPairSerializer,
    CategorySerializer,
    NotePatchSerializer,
    NoteSerializer,
    NoteViewSerializer,
    SharedItemSerializer,
    UserSerializer,
)
from .shortcuts import generate_jwt_token
from notes.models import Category, Note, SharedItem
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

        serializer = NoteViewSerializer(notes, many=True)
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

    permission_classes = (IsAuthenticated,)

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

        serializer = NoteViewSerializer(note)
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

        serializer = NotePatchSerializer(instance=note, data=request.data)

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
            note = get_object_or_404(Note, uuid=note_id, author=user)
        except Http404:
            return Response(
                {'detail': 'Note not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NoteSharedItemList(generics.ListAPIView):
    serializer_class = SharedItemSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        note_id = self.kwargs['note_id']
        note = get_object_or_404(Note, uuid=note_id, author=self.request.user)
        return SharedItem.objects.filter(note=note)

    def post(self, request, note_id):
        note = get_object_or_404(Note, uuid=note_id, author=self.request.user)
        serializer = SharedItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(note=note)
            return Response(
                {'data': serializer.data, 'detail': 'Note permission supdated successfully'},
                status=status.HTTP_201_CREATED,  # TODO: make it so it does proper status
            )
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, note_id):
        note = get_object_or_404(Note, uuid=note_id, author=self.request.user)
        serializer = SharedItemSerializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        SharedItem.objects.filter(note=note).delete()

        serializer.save(note=note)
        return Response(
            {'data': serializer.data, 'detail': 'Note permissions updated successfully'},
        )

    def patch(self, request, note_id):
        note = get_object_or_404(Note, uuid=note_id, author=self.request.user)
        serializer = SharedItemSerializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(note=note)
        return Response(
            {'data': serializer.data, 'detail': 'Note permissions updated successfully'},
        )

    def delete(self, request, note_id):
        note = get_object_or_404(Note, uuid=note_id, author=self.request.user)
        SharedItem.objects.filter(note=note).delete()
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


class CurrentUserView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True)

    def get_object(self):
        return get_object_or_404(self.queryset, username=self.kwargs['username'])


@api_view(['GET'])
def user_search(request):
    NUM_USERS_MAX = 5
    LEN_QUERY_MIN = 3
    query = request.query_params.get('search_query')
    if not query:
        return Response({'data': []})

    qs = User.objects.filter(is_active=True)
    if len(query) < LEN_QUERY_MIN:
        users = qs.filter(username=query)[:1]
    else:
        users = qs \
            .filter(username__startswith=query) \
            .order_by('username')[:NUM_USERS_MAX + 1]  # ordering guarantees that first object is closest match (maybe)
        if len(users) > NUM_USERS_MAX:
            if users[0].username == query:
                # the closest match is an exact match, that's the only one we'll need
                users = [users[0]]
            else:
                users = []
    serializer = UserSerializer(users, many=True)
    return Response({'data': serializer.data})


@api_view(['POST'])
def register(request):
    serializer = AuthUserSerializer(data=request.data)

    if serializer.is_valid():
        # XXX: maybe use User.create_user instead
        serializer.validated_data['password'] = make_password(
            serializer.validated_data['password']
        )
        serializer.save()
        return Response(
            {'data': serializer.data, 'detail': 'User registered successfully'},
            status=status.HTTP_201_CREATED,
        )

    return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def summarize(request):
    if len(request.data['text']) < 50:
        return Response(
            {'message': 'Text too short for proper summarization'},
            status=status.HTTP_406_NOT_ACCEPTABLE
        )
    return Response(sum_text(request.data['text']))


@api_view(['POST'])
def genquest(request):
    return Response(gen_quest(request.data['text']))


def subject(request):
    return Response(text_subject(request.data['text']))


def quality(request):
    return Response(text_quality(request.data['text']))


class UserTokenPairView(TokenObtainPairView):
    serializer_class = AuthUserTokenObtainPairSerializer

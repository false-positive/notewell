from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from notes.models import Category, Note, SharedItem
from notes.serializers import NoteViewSerializer, NoteSerializer, NotePatchSerializer, SharedItemSerializer, \
    CategorySerializer, QuizSerializer
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
        quiz_data = {}
        quiz_data['content'] = request.data.pop('quiz', None)
        if quiz_data['content'] != None:
            quiz_data['note'] = note.pk
            quiz_serializer = QuizSerializer(instance=note.quiz_set.first(), data=quiz_data)
            if quiz_serializer.is_valid():
                quiz_serializer.save()
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

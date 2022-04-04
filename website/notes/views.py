import math
from itertools import chain

from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseNotAllowed
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Note, SharedItem
from .forms import CreateCommentForm
from .serializers import NoteViewSerializer, NoteSerializer, NotePatchSerializer, SharedItemSerializer, \
    CategorySerializer
from .shortcuts import get_accessible_note_or_404, get_notes, search
from api.shortcuts import generate_jwt_token

# TODO: Rewrite all of these views pretty much

from api.shortcuts import generate_jwt_token
import requests

def index(request, cat_path=None):
    # XXX: This code is *insanely* scuffed
    # should probably be rewritten
    if request.method != "GET":
        return HttpResponseNotAllowed('Only GET method is allowed!')  # no. NEVER do this!

    title = 'Public Notes'

    # TODO: escape the string
    # TODO: make search bar more advanced and maybe filter from category
    search_query = request.GET.get('search_query', None)
    if search_query:
        return search(request, search_query)

    if cat_path:
        try:
            category: Category = get_object_or_404(Category, full_path=cat_path)
        except Http404:
            raise Http404('Category not found')

        notes_res = get_notes(request, category)
        title = category.name
    else:
        notes_res = get_notes(request)

    notes = notes_res['notes']
    categories = Category.objects.all()

    current_page = notes_res['current_page']
    previous_page = current_page - 1
    next_page = current_page + 1

    if current_page <= 1:
        previous_page = 1
    elif current_page >= notes_res['page_count']:
        next_page = notes_res['page_count']

    return render(request, 'notes/note_list.html', {
        'title': title,
        'object_list': notes,
        'page': {
            'current': current_page,
            'previous': previous_page,
            'next': next_page,
            'count': notes_res['page_count'],
            'name': 'index',
        },
        'page_count_range': range(1, notes_res['page_count'] + 1),
        'categories': categories,
    })


@login_required
def my(request):
    notes = Note.objects.filter(author=request.user)
    categories = Category.objects.all()
    return render(request, 'notes/note_list.html', {
        'title': 'My Notes',
        'categories': categories,
        'object_list': notes,
        'page': {
            'name': 'my',
        }
    })


class NoteCreateView(LoginRequiredMixin, generic.CreateView):
    model = Note
    fields = ['title']  # TODO: categories

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def read(request, note_id):
    note: Note = get_accessible_note_or_404(request.user.pk, uuid=note_id)

    create_comment_form = CreateCommentForm()
    if request.method == "POST":
        create_comment_form = CreateCommentForm(request.POST)
        print(request.user)
        print(create_comment_form.is_valid())
        print(create_comment_form.errors)
        if create_comment_form.is_valid():
            instance = create_comment_form.save(commit=False)
            
            instance.note = note
            instance.author = request.user

            instance.save()

            return redirect(request.path_info)

    return render(request, 'notes/read.html', {
        'title': note.title,
        'note': note,
        'comments': note.comment_set.order_by('-creation_date'),
        'create_comment_form': create_comment_form,
        'categories': Category.objects.all(),
    })


@login_required
def edit(request, note_id):
    note: Note = get_accessible_note_or_404(request.user.pk, uuid=note_id)
    if not note.can_be_edited_by(request.user):
        read_url = reverse('notes:read', kwargs={'note_id': note_id})
        return redirect(read_url)

    token_pair = generate_jwt_token(request.user)

    return render(request, 'notes/edit.html', {
        'title': note.title,
        'note': note,
        'token_pair': token_pair,
        'open_dialog': request.GET.get('open_dialog', ''),
    })


@login_required
def publish(request, note_id):
    note: Note = get_accessible_note_or_404(request.user.pk, uuid=note_id)
    if request.method == 'POST':
        note.status = Note.PUBLIC
        if request.user.is_staff:
            note.verified = True
        note.save()
        read_url = reverse('notes:read', kwargs={'note_id': note_id})
        return redirect(read_url)
    return render(request, 'notes/note_confirm_publish.html', {'object': note})


class NoteDeleteView(generic.DeleteView):
    model = Note
    success_url = reverse_lazy('notes:index')

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = Note.objects
        note_id = self.kwargs['note_id']
        user = self.request.user
        return queryset.get(uuid=note_id, author=user)


def category(request, cat_path):
    if not Category.objects.filter(full_path=cat_path).exists:
        raise Http404('Category not found')

    cat_slug = cat_path.split('/')[-1]
    category: Category = get_object_or_404(Category, slug=cat_slug)
    categories = Category.objects.all()

    # TODO: figure out how to make a join or something here

    notes = []

    def get_all_child_notes(category):
        queryset = Note.objects \
            .filter(categories=category) \
            .filter_accessible_notes_by(user_pk=request.user.pk)
        for note in queryset:
            notes.append(note)

        for cat in category.children.all():
            get_all_child_notes(cat)

    get_all_child_notes(category)

    return render(request, 'notes/note_list.html', {
        'title': category.name,
        'categories': categories,
        'object_list': notes,
        'page': {
            'name': 'category',
        }
    })


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
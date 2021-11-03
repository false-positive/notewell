import math
from itertools import chain

from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, response

from rest_framework.response import Response

from .models import Category, Note
from .forms import CreateCommentForm
from .shortcuts import get_accessible_note_or_404

from api.shortcuts import generate_jwt_token
import requests


def index(request, cat_path=None):
    if request.method != "GET":
        raise "Only GET method is allowed!"

    # TODO escape the string
    # TODO make search bar more advanced and maybe filter from category
    search_query = request.GET.get('search_query', None)
    if search_query:
        return search(request, search_query)

    if cat_path:
        try:
            category: Category = get_object_or_404(Category, full_path=cat_path)
        except Http404:
            raise Http404('Category not found')

        notes_res = get_notes(request, category)
    else:
        notes_res = get_notes(request)

    notes = notes_res['notes']
    categories = Category.objects.all()

    return render(request, 'notes/note_list.html', {
        'title': 'Public Notes',
        'object_list': notes,
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
        if create_comment_form.is_valid():
            instance = create_comment_form.save(commit=False)
            instance.note = note
            instance.save()

            return redirect(request.path_info)

    return render(request, 'notes/read.html', {
        'title': note.title,
        'note': note,
        'create_comment_form': create_comment_form,
    })


@login_required
def question(request, note_id):
    note: Note = get_accessible_note_or_404(request.user.pk, uuid=note_id)

    # parameters = {"input_text": "I have to save this coupon in case I come back to the store tomorrow.", "type": "MCQ"}
    parameters = {
        "input_text": note.content,
        "type": "MCQ"
    }

    response = requests.post("http://localhost:5000/generate_question", json=parameters)

    print(response.text)

    notes = Note.objects.filter(author=request.user)
    categories = Category.objects.all()
    return render(request, 'notes/note_list.html', {
        'title': 'Public Notes',
        'object_list': notes,
        'categories': categories,
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
    })


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
    })


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


def get_notes(request, category=None):

    # TODO maybe fix limit bug
    notes_on_page = int(request.GET.get('limit', 10))
    page_num = int(request.GET.get('p', 1))

    start = notes_on_page * (page_num - 1)
    end = notes_on_page * page_num

    if category:
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
            .filter_accessible_notes_by(user_pk=request.user.pk)

    # TODO maybe find a better way to return the values

    return {
        "notes": notes[start:end],
        "page_count": math.ceil(notes.count() / notes_on_page)
    }

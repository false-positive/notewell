import math
from itertools import chain

from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseNotAllowed

from .models import Category, Note
from .forms import CreateCommentForm
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

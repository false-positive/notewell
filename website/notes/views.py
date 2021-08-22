from itertools import chain
from django.views import generic
from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from .models import Category, Note
from .forms import CreateCommentForm
from .shortcuts import get_accessible_note_or_404


def index(request):
    if request.method == "GET":
        # TODO escape the string
        # TODO make search bar more advanced
        search_query = request.GET.get('search_query', None)
        if search_query:
            return search(request, search_query)

    notes = Note.objects \
        .select_related('author') \
        .filter(status="public")
    categories = Category.objects.all()
    return render(request, 'notes/note_list.html', {
        'title': 'Public Notes',
        'object_list': notes,
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


@login_required
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
def edit(request, note_id):
    note: Note = get_accessible_note_or_404(request.user.pk, uuid=note_id)
    if not note.can_be_edited_by(request.user):
        read_url = reverse('notes:read', kwargs={'note_id': note_id})
        return redirect(read_url)

    return render(request, 'notes/edit.html', {
        'title': note.title,
        'note': note,
    })


@login_required
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

    notes_by_title = Note.objects.filter(title__icontains=search_query, status='public')
    notes_by_author = Note.objects.filter(author__username__icontains=search_query, status='public')

    notes = set(chain(notes_by_title, notes_by_author))

    return render(request, 'notes/note_list.html', {
        'title': f'Search results for "{search_query}"',
        'categories': Category.objects.all(),
        'object_list': notes,
    })

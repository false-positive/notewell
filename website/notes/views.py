from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Category, Note
from .forms import CreateCommentForm
from .shortcuts import get_accessible_note_or_404


def index(request):
    user_pk = request.user.pk
    notes = Note.objects \
        .select_related('author') \
        .filter_accessible_notes_by(user_pk=user_pk)
    categories = Category.objects.all()
    return render(request, 'notes/note_list.html', {
        'title': 'Public Notes',
        'object_list': notes,
        'categories': categories,
    })


def my(request):
    notes = Note.objects.filter(author=request.user)
    categories = Category.objects.all()
    return render(request, 'notes/note_list.html', {
        'title': 'My Notes',
        'categories': categories,
        'object_list': notes,
    })


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


def category(request, cat_path):
    path_exists = False
    for cat in Category.objects.all():
        if cat.get_full_path() == cat_path:
            path_exists = True

    if not path_exists:
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

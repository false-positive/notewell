from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import BulletPoint, Category, Comment, Note
from .forms import CreateCommentForm


def index(request):
    notes = Note.objects.select_related('author')
    categories = Category.objects.all()
    return render(request, 'notes/index.html', {
        'title': 'Public Notes',
        'notes': notes,
        'categories': categories,
    })


def my(request):
    categories = Category.objects.all()
    return render(request, 'notes/my.html', {
        'title': 'My Notes',
        'categories': categories,
    })


@login_required
def read(request, note_id):
    note: Note = get_object_or_404(Note, uuid=note_id)
    if not note.can_be_read_by(request.user):
        raise Http404('Note not found')

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
        'categories': Category.objects.all(),
        'note': note,
        'create_comment_form': create_comment_form
    })


@login_required
def edit(request, note_id):
    note: Note = get_object_or_404(Note, uuid=note_id)
    if not note.can_be_edited_by(request.user):
        if note.can_be_read_by(request.user):
            read_url = reverse('notes:read', kwargs={'note_id': note_id})
            return redirect(read_url)
        raise Http404('Note not found')
    return render(request, 'notes/edit.html', {'title': note.title, 'note': note})


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
        for note in Note.objects.filter(categories=category):
            notes.append(note)

        for cat in category.children.all():
            get_all_child_notes(cat)

    get_all_child_notes(category)

    return render(request, 'notes/category.html', {
        'title': category.name,
        'categories': categories,
        'notes': notes
    })

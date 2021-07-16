from django.shortcuts import redirect, render, get_object_or_404

from .models import Category, Comment, Note
from .forms import CreateCommentForm


def index(request):
    notes = Note.objects.all()
    return render(request, 'notes/index.html', {
        'title': 'Public Notes',
        'notes': notes,
        'categories': Category.objects.all(),
    })


def my(request):
    return render(request, 'notes/my.html', {
        'title': 'My Notes',
        'categories': Category.objects.all(),
    })


def read(request, note_id):
    note: Note = get_object_or_404(Note, uuid=note_id)

    comments = Comment.objects.filter(note=note.id)
    categories = Category.objects.all()

    create_comment_form = CreateCommentForm()
    if request.method == "POST":
        create_comment_form = CreateCommentForm(request.POST)
        if create_comment_form.is_valid():
            # Save comment to db
            instance = create_comment_form.save(commit=False)
            instance.note = note
            instance.save()

            # Empty form fields
            create_comment_form = CreateCommentForm()

    return render(request, 'notes/view.html', {
        'title': note.title,
        'categories': categories,
        'note': note,
        'comments': comments,
        'create_comment_form': create_comment_form
    })


def edit(request, note_id):
    note: Note = get_object_or_404(Note, uuid=note_id)
    return render(request, 'notes/edit.html', {'title': note.title, 'note': note})


def category(request, cat_path):
    pathExist = False
    for cat in Category.objects.all():
        if cat.get_full_path() == cat_path:
            pathExist = True

    if not pathExist:
        # TODO: Add a 404 page
        return redirect('/notes/')

    cat_slug = cat_path.split('/')[-1]
    category: Category = get_object_or_404(Category, slug=cat_slug)
    categories = Category.objects.all()

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

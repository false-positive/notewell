from django.shortcuts import redirect, render, get_object_or_404

from .models import Comment, Note
from .forms import CreateCommentForm


def index(request):
    notes = Note.objects.all()
    return render(request, 'notes/index.html', {'title': 'Public Notes', 'notes': notes})


def my(request):
    return render(request, 'notes/my.html', {'title': 'My Notes'})


def view(request, note_id):
    note: Note = get_object_or_404(Note, uuid=note_id)

    comments = Comment.objects.filter(note=note.id)

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
        'note': note,
        'comments': comments,
        'create_comment_form': create_comment_form
    })


def edit(request, note_id):
    note: Note = get_object_or_404(Note, uuid=note_id)
    return render(request, 'notes/edit.html', {'title': note.title, 'note': note})

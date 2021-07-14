from django.shortcuts import render, get_object_or_404

from .models import Note


def index(request):
    notes = Note.objects.all()
    return render(request, 'notes/index.html', {'title': 'Public Notes', 'notes': notes})


def my(request):
    return render(request, 'notes/my.html', {'title': 'My Notes'})


def view(request, note_id):
    note: Note = get_object_or_404(Note, uuid=note_id)
    return render(request, 'notes/view.html', {'title': note.title, 'note': note})


def edit(request, note_id):
    note: Note = get_object_or_404(Note, uuid=note_id)
    return render(request, 'notes/edit.html', {'title': note.title, 'note': note})

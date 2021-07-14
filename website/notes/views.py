from django.shortcuts import render


def index(request):
    return render(request, 'notes/index.html', {'title': 'Public Notes'})


def my(request):
    return render(request, 'notes/my.html', {'title': 'My Notes'})


def view(request, note_id):
    return render(request, 'notes/view.html', {'title': note_id, 'note_id': note_id})


def edit(request, note_id):
    return render(request, 'notes/edit.html', {'title': note_id, 'note_id': note_id})

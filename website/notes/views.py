from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse('you decide what you put in the index')


def my(request):
    return HttpResponse('<h1>your notes show up here :)</h1>')


def view(request, note_id):
    # XXX: XSS vuln
    return HttpResponse(f'you are viewing note <em>{note_id}</em>')

def edit(request, note_id):
    # XXX: XSS vuln
    return HttpResponse(f'you are editing note <em>{note_id}</em>')

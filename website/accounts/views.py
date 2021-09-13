from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404

from notes.shortcuts import get_notes, search
from notes.models import Category

from .forms import UserLoginForm, UserRegisterForm


def profile(request, username):
    if request.method != "GET":
        raise "Only GET method is allowed!"

    # TODO escape the string
    # TODO make search bar more advanced and maybe filter from category

    user = get_object_or_404(User, username=username)

    notes_res = get_notes(request, user=user)

    notes = notes_res['notes']
    categories = Category.objects.all()

    current_page = notes_res['current_page']
    previous_page = current_page - 1
    next_page = current_page + 1

    if current_page <= 1:
        previous_page = 1
    elif current_page >= notes_res['page_count']:
        next_page = notes_res['page_count']

    return render(request, 'accounts/profile.html', {
        'title': f"{user.username}'s Public Notes",
        'object_list': notes,
        'page': {
            'current': current_page,
            'previous': previous_page,
            'next': next_page,
            'count': notes_res['page_count'],
        },
        'page_count_range': range(1, notes_res['page_count'] + 1),
        'categories': categories,
        'username': username,
    })


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # TODO: Maybe add `Success` message here
            return redirect('accounts:login')
        else:
            for field, errors in form.errors.as_data().items():
                # print(f'{field}: {errors[0]}')
                form.fields[field].widget.attrs['data-nw-error'] = errors[0].message

    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

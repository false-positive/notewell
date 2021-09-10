from django.shortcuts import render, redirect

from .forms import UserLoginForm, UserRegisterForm


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

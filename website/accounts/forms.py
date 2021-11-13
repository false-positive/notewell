from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import views as auth_views


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'mdc-text-field__input'
            self.fields[field].widget.attrs['aria-labelledby'] = 'my-label-id'
            # self.fields[field].widget.attrs['data-nw-error'] = 'test'

        self.fields['password1'].widget.attrs['minlength'] = '8'
        self.fields['password2'].widget.attrs['minlength'] = '8'


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'mdc-text-field__input'
            self.fields[field].widget.attrs['aria-labelledby'] = 'my-label-id'

        self.fields['password'].widget.attrs['minlength'] = '8'

        self.error_messages['invalid_login'] = 'Please enter a correct username and password.'

from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm

from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', authentication_form=UserLoginForm), name='login'),  # noqa
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),  # noqa
]

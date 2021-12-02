from django.urls import path
from django.contrib.auth.views import LoginView

from .forms import UserLoginForm
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='accounts/login.html', authentication_form=UserLoginForm), name='login'),
    path('logout/', views.logout, name='logout'),

    path('user/<path:username>/', views.profile, name='profile'),
]

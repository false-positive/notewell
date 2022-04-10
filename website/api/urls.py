from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path('token/', views.UserTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('user_search/', views.user_search, name='user_search'),

    path('user/', views.CurrentUserView.as_view(), name='user_current'),
    path('user/<str:username>/', views.UserView.as_view(), name='user_detail'),

    path('register/', views.register, name='register'),

    path('ai/summarize/', views.summarize, name='summarize'),
    path('ai/questgen/', views.genquest, name='questgen'),
    path('ai/quality/', views.quality, name='quality'),
    path('ai/subject/', views.subject, name='subject'),

    path('', include('notes.urls.api')),
]

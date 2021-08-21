from django.urls import path
from . import views

# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # path('users/', views.UserAPIView.as_view()),
    path('users/', views.view_users, name='user-list'),

    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),

    path('notes/', views.note_crud),
    path('notes/<uuid:note_id>/', views.note_crud),

    path('categories/', views.view_categories, name='category-list-all'),
    path('categories/<path:cat_path>/',
         views.view_categories, name='category-detail'),

    path('notes/all/', views.view_notes, name='note-list-detail'),
    path('notes/c/<path:cat_path>/', views.view_notes, name='note-list-detail'),

]

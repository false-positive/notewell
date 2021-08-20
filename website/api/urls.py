from django.urls import path
from . import views

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('users/', views.view_users, name='user-list'),

    path('login/', obtain_auth_token, name='login'),
    path('register/', views.register, name='register'),

    path('notes/', views.note_crud, name='note-crud'),
    path('notes/<uuid:note_id>/', views.note_crud, name='note-detail'),
    path('notes/<uuid:note_id>/', views.note_crud, name='note-update'),
    path('notes/<uuid:note_id>/', views.note_crud, name='note-delete'),

    path('categories/', views.view_categories, name='category-list-all'),
    path('categories/<path:cat_path>/',
         views.view_categories, name='category-detail'),
    path('notes/<path:cat_path>/notes/', views.view_notes, name='note-list-detail'),
    path('test', views.test, name='test'),
]

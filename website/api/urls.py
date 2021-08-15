from django.urls import path
from . import views

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('users/', views.view_users, name='user-list'),
    #     path('user/', views.view_notes, name='note-list-all'),

    path('login/', obtain_auth_token, name='login'),
    path('register/', views.register, name='register'),

    path('notes/', views.view_notes, name='note-list-all'),
    path('notes/<path:cat_path>/', views.view_notes, name='note-list-detail'),
    path('note/', views.note_crud, name='note-create'),
    path('note/<uuid:note_id>/', views.note_crud, name='note-detail'),
    path('note/<uuid:note_id>/', views.note_crud, name='note-update'),
    path('note/<uuid:note_id>/', views.note_crud, name='note-delete'),

    path('categories/', views.view_categories, name='category-list-all'),
    path('categories/<path:cat_path>/',
         views.view_categories, name='category-detail')
]

from django.urls import path
from . import views

urlpatterns = [
    path('notes/', views.view_notes, name='note-list-all'),
    path('notes/<path:cat_path>/', views.view_notes, name='note-list-detail'),
    path('note/<uuid:note_id>/', views.view_note, name='note-detail'),
    path('categories/',
         views.view_categories, name='category-list-all'),
    path('categories/<path:cat_path>/',
         views.view_categories, name='category-list-detail')
]

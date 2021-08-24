from django.urls import path

from . import views


app_name = 'notes'
urlpatterns = [
    path('', views.index, name='index'),
    path('my/', views.my, name='my'),
    path('new/', views.NoteCreateView.as_view(), name='create'),
    path('<uuid:note_id>/view/', views.read, name='read'),
    path('<uuid:note_id>/edit/', views.edit, name='edit'),
    path('<path:cat_path>/', views.index, name='category'),
]

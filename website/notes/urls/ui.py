from django.urls import path

from notes.views import ui as views


app_name = 'notes'
urlpatterns = [
    path('', views.index, name='index'),
    path('my/', views.my, name='my'),
    path('new/', views.NoteCreateView.as_view(), name='create'),
    path('<uuid:note_id>/', views.read, name='read'),
    path('<uuid:note_id>/edit/', views.edit, name='edit'),
    path('<uuid:note_id>/delete/', views.NoteDeleteView.as_view(), name='delete'),
    path('<uuid:note_id>/publish/', views.publish, name='publish'),
    path('<path:cat_path>/', views.index, name='category'),
]

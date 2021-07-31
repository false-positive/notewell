from django.urls import path

from . import views


app_name = 'notes'
urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.NoteListView.as_view(), name='index'),
    path('my/', views.my, name='my'),
    path('<uuid:note_id>/view/', views.read, name='read'),
    path('<uuid:note_id>/edit/', views.edit, name='edit'),
    path('<path:cat_path>/', views.category, name='category'),
]

from django.urls import path

from . import views


app_name = 'notes'
urlpatterns = [
    path('', views.index, name='index'),
    path('my/', views.my, name='my'),
    path('<str:note_id>/view/', views.view, name='view'),
    path('<str:note_id>/edit/', views.edit, name='edit'),
]
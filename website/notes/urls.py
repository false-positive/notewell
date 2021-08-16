from django.urls import path
from django.views.generic import TemplateView

from . import views


app_name = 'notes'
urlpatterns = [
    path('', views.index, name='index'),
    path('my/', views.my, name='my'),
    path('<uuid:note_id>/view/', views.read, name='read'),
    path('<uuid:note_id>/edit/',
         TemplateView.as_view(template_name="notes/editor.html"), name='edit'),
    path('<path:cat_path>/', views.category, name='category'),
]

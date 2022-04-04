from django.urls import path

import notes.views.api

app_name = 'notes_api'
urlpatterns = [
    path('notes/', notes.views.api.NoteList.as_view(), name='note_list'),
    path('notes/<uuid:note_id>/', notes.views.api.NoteDetail.as_view(), name='note_detail'),
    path('notes/<uuid:note_id>/permissions/',
         notes.views.api.NoteSharedItemList.as_view(), name='note_shareditem_list'),

    path('categories/', notes.views.api.view_categories, name='category_list'),
    path('categories/<path:cat_path>/', notes.views.api.view_categories, name='category_detail'),
]

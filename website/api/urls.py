from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

import notes.views
from . import views

urlpatterns = [
    path('token/', views.UserTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('user_search/', views.user_search, name='user_search'),

    path('user/', views.CurrentUserView.as_view(), name='user_current'),
    path('user/<str:username>/', views.UserView.as_view(), name='user_detail'),

    path('register/', views.register, name='register'),

    path('ai/summarize/', views.summarize, name='summarize'),
    path('ai/questgen/', views.genquest, name='questgen'),
    path('ai/quality/', views.quality, name='quality'),
    path('ai/subject/', views.subject, name='subject'),

    path('notes/', notes.views.NoteList.as_view(), name='note_list'),
    path('notes/<uuid:note_id>/', notes.views.NoteDetail.as_view(), name='note_detail'),
    path('notes/<uuid:note_id>/permissions/',
         notes.views.NoteSharedItemList.as_view(), name='note_shareditem_list'),

    path('categories/', notes.views.view_categories, name='category_list'),
    path('categories/<path:cat_path>/', notes.views.view_categories, name='category_detail'),
]

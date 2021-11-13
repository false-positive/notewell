from django.urls import path
from . import views

# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/', views.UserTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('user_search/', views.user_search, name='user_search'),

    path('user/', views.CurrentUserView.as_view(), name='user_current'),
    path('user/<str:username>/', views.UserView.as_view(), name='user_detail'),

    path('register/', views.register, name='register'),

    path('notes/summarize/', views.summarize(), name='summarize'),
    path('notes/questgen/', views.genquest(), name='questgen'),
    path('notes/quality/', views.quality(), name='quality'),
    path('notes/subject/', views.subject(), name='subject'),

    path('notes/', views.NoteList.as_view(), name='note_list'),
    path('notes/<uuid:note_id>/', views.NoteDetail.as_view(), name='note_detail'),
    path('notes/<uuid:note_id>/permissions/',
         views.NoteSharedItemList.as_view(), name='note_shareditem_list'),

    path('categories/', views.view_categories, name='category_list'),
    path('categories/<path:cat_path>/', views.view_categories, name='category_detail'),
]

"""notewell_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView
import debug_toolbar

admin.site.site_header = 'Notewell Administration'
admin.site.index_title = 'Admin'

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('notes:index')), name='index'),
    path('', include('accounts.urls')),
    path('notes/', include('notes.urls.ui')),
    path('api/', include('api.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),
]

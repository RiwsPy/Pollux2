"""pollux URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, re_path
from .views import index, show_map, print_json, MentionsLegales, About, ShowMapDescription

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    re_path(r'map/(?P<map_id>\w+)$', show_map),
    re_path(r'api/(.+)', print_json),
    path('mentions_legales', MentionsLegales.as_view(), name='mentions_legales'),
    path('about', About.as_view(), name="about"),
    re_path(r'map_desc/(.+)', ShowMapDescription.as_view(), name='map_description'),
]

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
from .views import index, show_map, print_json, mentions_legales, about, show_map_description

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    re_path(r'map/(?P<map_id>\w+)$', show_map),
    re_path(r'api/(.+)', print_json),
    path('mentions_legales', mentions_legales, name='mentions_legales'),
    path('about', about, name="about"),
    re_path(r'map_desc/(.+)', show_map_description, name='map_description'),
]

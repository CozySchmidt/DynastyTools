# from django.contrib.auth import views
from django.urls import path, re_path, include
from .views import *
from rankingsApp import views
from django.conf.urls import url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', UploadView.as_view(), name='upload'),
    re_path(r'', views.ReactAppView.as_view())
]

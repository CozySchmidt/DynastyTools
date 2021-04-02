# from django.contrib.auth import views
from django.urls import path, re_path, include
from .views import *
from rankingsApp import views
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^', views.ReactAppView.as_view())
]


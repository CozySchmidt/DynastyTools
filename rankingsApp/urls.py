# from django.contrib.auth import views
from django.urls import path, re_path
from .views import *
from rankingsApp import views

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('admin/', AdminView.as_view(), name='admin'),
    re_path(r'^api/nextmatchup/$', views.GetNextMatchup)
]


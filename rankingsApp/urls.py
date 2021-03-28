from django.contrib.auth import views
from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('admin/', AdminView.as_view(), name='admin')
]


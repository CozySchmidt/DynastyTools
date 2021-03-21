from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index, name='Index'),
    path('PostMatchup', views.PostMatchup, name='PostMatchup')
]


from django.urls import path
from .views import Home
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('new_post', views.create_post, name='create_post'),
    path('', Home.as_view(), name='home')
]

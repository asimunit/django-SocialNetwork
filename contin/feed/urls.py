from django.contrib import admin
from django.urls import path, include
from . import views
from . import views

urlpatterns=[
    path('', views.Home.as_view(), name='home'),
    path('post/new/', views.create_post, name='create_post'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.post_delete, name='post-delete'),
]
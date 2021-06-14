from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('post/new/', views.create_post, name='create_post'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post'
                                                                       '-update'),
    path('post/<int:pk>/delete/', views.post_delete, name='post-delete'),
    path('post/save/', views.save_post, name='post-save'),
    path('post/<int:pk>/space_ner/', views.name_entity_recognition_spacy,
         name='name_entity_recognition_spacy'),
    path('post/<int:pk>/stanford_ner/', views.name_entity_recognition_stanford,
         name='name_entity_recognition_stanford'),
    path('post/<int:pk>/stanford_ner_cmd/', views.name_entity_recognition_cmd,
         name='name_entity_recognition_cmd'),
]

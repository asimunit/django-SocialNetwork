from django.urls import path
from . import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', user_views.register, name='register'),
    path('login/',
         auth_views.LoginView.as_view(template_name='account/login.html'),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('my_profile/', user_views.my_profile, name='my_profile'),
    path('update_profile/', user_views.update_profile, name='update_profile'),
    path('friend_list/', user_views.friend_list, name='friend_list'),
    path('my_invites/', user_views.invites_received, name='my_invites_view'),
    path('all_profile/', user_views.profile_list, name='all_profile'),
    path('user_profile/', user_views.user_profile,
         name='user_profile'),
    path('send_invite/', user_views.add_friend, name='send_invite'),
    path('remove_friend/', user_views.remove_friend, name='remove_friend'),
    path('accept_invitation/', user_views.accept_invitation,
         name='accept_invitation'),
    path('reject_invitation/', user_views.reject_invitation,
         name='reject_invitation'),
    path('search_users/', user_views.search_users, name='search_users'),

]

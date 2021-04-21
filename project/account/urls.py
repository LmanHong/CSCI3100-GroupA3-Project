from django.contrib import admin
from django.urls import path, include

import account.views

# all url paths for account module
urlpatterns = [
    path('profile/', account.views.ProfileView.as_view(), name='profile'),
    path('register/', account.views.RegistrationView.as_view(), name='register'),
    path('login/', account.views.LoginView.as_view(), name='login'),
    path('logout/', account.views.LogoutView.as_view(), name='logout'),
    path('profile_update/', account.views.profile_update, name='profile_update'),
]

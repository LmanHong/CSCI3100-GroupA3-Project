from django.contrib import admin
from django.urls import path, include

import account.views

urlpatterns = [
    path('profile/', account.views.ProfileView.as_view(), name='profile'),
    path('register/', account.views.RegistrationView.as_view(), name='register'),
]

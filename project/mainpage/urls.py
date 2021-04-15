from django.contrib import admin
from django.urls import path

import mainpage.views
import chat.views
import friendSearch.views
import account.views

urlpatterns = [
    path('', mainpage.views.main_page.as_view(), name='mainpage'),
    path('chat/', chat.views.HomeView.as_view(), name='chat'),
    path('frdSearch/', friendSearch.views.FriendSearchView.as_view(), name='friendSearch'),
    path('register/', account.views.RegistrationView.as_view(), name='register'),
    path('account_setting/', account.views.profile_update, name='account_setting'),
    path('login/', account.views.LoginView.as_view(), name='login'),
]

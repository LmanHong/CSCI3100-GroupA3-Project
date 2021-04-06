from django.contrib import admin
from django.urls import path

import friendSearch.views

urlpatterns = [
    path('frdList/', friendSearch.views.FriendListView.as_view(), name='friendList'),
    path('frdSearch/', friendSearch.views.FriendSearchView.as_view(), name='friendSearch'),
    path('request/',friendSearch.views.RequestView.as_view(), name='request'),

]

from django.contrib import admin
from django.urls import path

import friendSearch.views

urlpatterns = [
    path('frdList/', friendSearch.views.FriendList.as_view(), name='friendList'),
    path('frdSearch/', friendSearch.views.FriendSearch.as_view(), name='friendSearch'),

]

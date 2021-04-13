from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

import friendSearch.views

urlpatterns = [
    #path('frdList/', friendSearch.views.FriendListView.as_view(), name='friendList'),
    path('frdSearch/', friendSearch.views.FriendSearchView.as_view(), name='friendSearch'),
    path('request/',friendSearch.views.RequestView.as_view(), name='request'),

]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

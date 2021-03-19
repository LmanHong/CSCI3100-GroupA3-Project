from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import chat.views

urlpatterns = [
    path('', chat.views.HomeView.as_view(), name="index"),
    path('<str:room_name>/', chat.views.ChatRoomView.as_view(), name='chatroom')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

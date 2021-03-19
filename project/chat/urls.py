from django.urls import path, include

import chat.views

urlpatterns = [
    path('', chat.views.HomeView.as_view(), name="index"),
    path('<str:room_name>/', chat.views.ChatRoomView.as_view(), name='chatroom')
]

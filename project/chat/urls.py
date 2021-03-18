from django.urls import path, include

import chat.views

urlpatterns = [
    path('', chat.views.index, name="index"),
    path('<str:room_name>/', chat.views.ChatRoomView.as_view(), name='chatroom')
]

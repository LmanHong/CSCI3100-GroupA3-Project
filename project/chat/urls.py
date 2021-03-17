from django.urls import path, include

import chat.views

urlpatterns = [

    path('', chat.views.chat_room, name='chatroom')
]

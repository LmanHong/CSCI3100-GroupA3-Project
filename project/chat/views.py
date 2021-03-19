from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ChatRoom, ChatMessage

import json

LOGIN='/account/login/'

class HomeView(LoginRequiredMixin, View):
    login_url=LOGIN
    def get(self, request, *args, **kwargs):
        return render(request, 'chat/index.html')

    def post(self, request, *args, **kwargs):
        if request.POST['username']:
            pass
        return redirect('/chat')

class ChatRoomView(LoginRequiredMixin, View):
    login_url=LOGIN

    def get(self, request, *args, **kwargs):
        room_name = self.kwargs['room_name']
        return render(request, 'chat/chatroom.html', {
            'room_name':room_name
        })
    
    def post(self, request, *args, **kwargs):
        room_name = self.kwargs['room_name']
        body = json.loads(request.body.decode('utf-8'))
        message_string = body["message_string"]
        message_status = body["message_status"]
        sent_time = body["sent_time"]
        if (message_string and message_status and sent_time): status = True
        else: status = False
        info_str = "Got information from room {}: {}, sent at {}, status is {}.".format(room_name, message_string, sent_time, message_status)
        print(info_str)
        return JsonResponse({
            'status': status,
            'info_str': info_str
        })



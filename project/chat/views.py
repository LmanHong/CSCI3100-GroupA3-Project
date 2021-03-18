from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from .models import ChatRoom, ChatMessage

import json

def index(request):
    return render(request, 'chat/index.html')

class ChatRoomView(View):
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

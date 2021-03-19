from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from .models import ChatRoom, ChatMessage


import json

LOGIN='/account/login/'

class HomeView(LoginRequiredMixin, View):
    login_url=LOGIN
    def get(self, request, *args, **kwargs):
        return render(request, 'chat/index.html')

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            body = json.loads(request.body.decode('utf-8'))
            to_username = body["to_username"]
            try:
                new_room = ChatRoom.objects.create_chatroom(from_username=user.username, to_username=to_username)
                responseBody = {
                    'status':True,
                    'room_name':new_room.room_name
                }
            except Exception as ex:
                err = "Exception of type {0} occured when creating chatroom, Arguments:\n{1!r}".format(type(ex).__name__, ex.args)
                print(err)
                responseBody = {
                    'status':False,
                    'error': err
                }
        else:
            err = 'User not logged in.'
            print(err)
            responseBody = {
                'status':False,
                'error': err
            }
        return JsonResponse(responseBody)



class ChatRoomView(LoginRequiredMixin, View):
    login_url=LOGIN

    def get(self, request, *args, **kwargs):
        room_name = self.kwargs['room_name']
        from_user = request.user
        try:
            target_room = ChatRoom.objects.get_chatroom(int(room_name))
            if (target_room.from_user != from_user and target_room.to_user != from_user): raise ObjectDoesNotExist
            else:
                context = {
                    'room_name':room_name
                }
        except Exception as ex:
            err = "Exception of type {0} occured when creating chatroom, Arguments:\n{1!r}".format(type(ex).__name__, ex.args)
            print(err)
            context = {
                'error':err
            }
        return render(request, 'chat/chatroom.html', context)
    
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



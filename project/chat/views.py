from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.views.decorators.clickjacking import xframe_options_sameorigin
from .models import ChatRoom, ChatMessage
from friendSearch.models import FriendList


import re
import json

LOGIN='/account/login/'

class HomeView(LoginRequiredMixin, View):
    login_url=LOGIN
    def get(self, request, *args, **kwargs):
        user = request.user
        friendList = FriendList.objects.returnFriendList(user=user)
        print(len(friendList))
        friendProfileList = [get_user_model().objects.get(username=friend['username']) for friend in friendList]
        context = {
            'friendList': friendProfileList,
            'friendCount': len(friendProfileList)
        }
        return render(request, 'chat/index.html', context)

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            body = json.loads(request.body.decode('utf-8'))
            to_user_id = body["to_user_id"]
            try:
                to_user = get_user_model().objects.get(id=to_user_id)
                new_room = ChatRoom.objects.create_chatroom(from_username=user.username, to_username=to_user.username)
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

    @xframe_options_sameorigin
    def get(self, request, *args, **kwargs):
        room_name = self.kwargs['room_name']
        from_user = request.user
        try:
            target_room = ChatRoom.objects.get_chatroom(int(room_name))
            message_set = ChatMessage.objects.get_messages_from_chatroom(int(room_name))
            message_list = [{
                'message_id': message.id,
                'message_string':message.message_string,
                'message_status':message.message_status,
                'error':message.error,
                'sent_by':message.sent_by,
                'sent_time':message.sent_time
            } for message in message_set]
            print("To User: {}".format(target_room.to_user.username))
            print(target_room.to_user.profile)
            if (target_room.from_user != from_user and target_room.to_user != from_user): raise ObjectDoesNotExist
            else:
                context = {
                    'room_name':room_name,
                    'to_user': target_room.to_user if target_room.from_user == from_user else target_room.from_user,
                    'message_list': message_list
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
        message_status = body["message_status"]
        sent_time = body["sent_time"]
        if (message_status == 'msg'):
            message_string = body["message_string"]
            chat_room = ChatRoom.objects.get_chatroom(room_name)
            if (message_string and message_status and sent_time and (chat_room.from_user==request.user or chat_room.to_user==request.user)):
                new_msg = ChatMessage.objects.create_message(chat_room=chat_room, sent_by=request.user.username, message_string=message_string)
                status = True
                info_str = "Got information from room {}: {}, sent at {}, status is {}. (message ID: {})".format(room_name, message_string, new_msg.sent_time, new_msg.message_status, new_msg.id)
            else: 
                status = False
                info_str = "Message format incorrect."
            print(info_str)
            response_json = {
                'status': status,
                'info_str': info_str
            }
        elif (message_status == 'spc'):
            special_request= body["special_request"]
            if (special_request and message_status and sent_time): status = True
            else: status = False
            if (status and re.match('^getMessage', special_request)):
                count = re.search('-[1-9][0-9]*$', special_request)
                print(count)
                if count: count = int(count.group()[1:])
                else: count = 0
                print('count: ',count)
                message_set = ChatMessage.objects.get_messages_from_chatroom(int(room_name))
                message_list = [{
                    'message_id':message.id,
                    'message_string':message.message_string,
                    'message_status':message.message_status,
                    'error':message.error,
                    'sent_by':message.sent_by,
                    'sent_time':message.sent_time
                } for message in message_set]
                print(message_list)
                response_json = {
                    'status':status,
                    'message_list':message_list,
                    'message_count':len(message_list)
                }
            else:
                info_str = "Request format incorrect."
                print(info_str)
                response_json = {
                    'status':status,
                    'info_str': info_str
                }
        else:
            info_str = "Unknown status."
            print(info_str)
            response_json = {
                'status': False,
                'info_str': info_str
            }
        return JsonResponse(response_json)




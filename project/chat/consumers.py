import json
from datetime import datetime
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import ChatRoom, ChatMessage
from django.core.serializers.json import DjangoJSONEncoder

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        #Get room name from url
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user = self.scope["user"]
        self.group_name = "group_{}".format(self.room_name)

        ChatRoom.objects.set_online_status(self.room_name, self.user.username, "Online")
        room = ChatRoom.objects.get_chatroom(self.room_name)
        to_username = room.from_user.username if self.user.username == room.to_user.username else room.to_user.username
        to_user_status = room.from_user_status if self.user.username == room.to_user.username else room.to_user_status


        #Add current chat user channel to the group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        #Accepts the incoming websocket connection
        self.accept()

        #Get others' online status
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type':'spc',
                'new_msg':{
                    'message_string': {'online_status': 'Online' if to_user_status else 'Offline'},
                    'message_status': 'spc',
                    'sent_time': str(datetime.now()),
                    'sent_by': to_username,
                }
            }
        )

        #Broadcase to others
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type':'spc',
                'new_msg': {
                    'message_string': {'online_status': 'Online'},
                    'message_status': 'spc',
                    'sent_time': str(datetime.now()),
                    'sent_by': self.user.username,
                }
            }
        )

    def disconnect(self, close_code):
        #Set Online status to Offline
        ChatRoom.objects.set_online_status(self.room_name, self.user.username, 'Offline')
        
        #Broadcase to others
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type':'spc',
                'new_msg': {
                    'message_string': {'online_status': 'Offline'},
                    'message_status': 'spc',
                    'sent_time': str(datetime.now()),
                    'sent_by': self.user.username,
                }
            }
        )

        #Leave the group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        #Receive messages from websocket
        chat_room = ChatRoom.objects.get_chatroom(self.room_name)
        text_data_json = json.loads(text_data)
        message_string = text_data_json['message_string']
        message_status = text_data_json['message_status']
        sent_time = text_data_json['sent_time']
        sent_by = self.user.username

        if message_status == 'msg':
            new_msg = ChatMessage.objects.create_message(chat_room=chat_room, sent_by=sent_by, message_string=message_string)

            #Send the received message to the group
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type': 'msg',
                    'new_msg': new_msg
                }
            )
        else:
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type':'spc',
                    'new_msg': {
                        'message_string': message_string,
                        'message_status': message_status,
                        'sent_time': sent_time,
                        'sent_by': sent_by,
                    }
                }
            )

    def spc(self, event):
        #Receive messages from group
        message_string = event['new_msg']['message_string']
        message_status = event['new_msg']['message_status']
        sent_time = event['new_msg']['sent_time']
        sent_by = event['new_msg']['sent_by']

        #Send message to websocket
        self.send(text_data=json.dumps({
            'message_string': message_string,
            'message_status': message_status,
            'sent_time': sent_time,
            'sent_by': sent_by
        }, cls=DjangoJSONEncoder))

    def msg(self, event):
        #Receive messages from group
        message_id = event['new_msg'].id
        message_string = event['new_msg'].message_string
        message_status = event['new_msg'].message_status
        sent_time = event['new_msg'].sent_time
        sent_by = event['new_msg'].sent_by

        #Send message to websocket
        self.send(text_data=json.dumps({
            'message_id': message_id,
            'message_string': message_string,
            'message_status': message_status,
            'sent_time': sent_time,
            'sent_by': sent_by
        }, cls=DjangoJSONEncoder))
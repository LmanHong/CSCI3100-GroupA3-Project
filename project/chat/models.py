from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

class ChatRoomManager(models.Manager):
    def get_chatroom(self, room_name=None,from_username=None, to_username=None, exact=False):
        if (not room_name and (not from_username or not to_username)):
            raise ValueError("Room Name and either username cannot be None together")
        elif room_name:
            return self.get_queryset().get(room_name=room_name)
        else:
            from_user = get_user_model().objects.get(username=from_username)
            to_user = get_user_model().objects.get(username=to_username)
            if not exact:
                rooms = self.get_queryset().filter((models.Q(from_user=from_user) & models.Q(to_user=to_user)) | (models.Q(from_user=to_user) & models.Q(to_user=from_user)))
                if len(rooms) == 0:
                    raise ObjectDoesNotExist
                elif len(rooms) > 1:
                    raise MultipleObjectsReturned
                else:
                    return rooms[0]
            else:
                return self.get_queryset().get(from_user=from_user, to_user=to_user)
    
    def get_all_chatrooms_by_user(self, from_username, query=None):
        if not from_username:
            raise ValueError("username cannot be None")
        else:
            from_user = get_user_model().objects.get(username=from_username)
            if not query:
                return self.get_queryset().filter(models.Q(from_user=from_user) | models.Q(to_user=from_user))
            else:
                return query.filter(models.Q(from_user=from_user) | models.Q(to_user=from_user))

    def create_chatroom(self, from_username, to_username):
        if from_username == "" or to_username == "" or from_username == to_username:
            raise ValueError("Chat Room must have two unique and non-empty usernames")
        else:
            from_user = get_user_model().objects.get(username=from_username)
            to_user = get_user_model().objects.get(username=to_username)
            try:
                room = self.get_chatroom(from_username=from_username, to_username=to_username)
                return room
            except MultipleObjectsReturned:
                raise ValueError("Duplicated Chatrooms found, need to fix before creating new chatroom")
            except:
                new_room = self.model(
                    from_user=from_user,
                    to_user=to_user
                )
                new_room.save()
                return new_room

    def set_online_status(self, room_name, username, status):
        if room_name == "" or username == "" or status == "":
            raise ValueError("All arguments must be non-empty")
        elif status != "Online" and status != "Offline":
            raise ValueError("Online Status must either be 'Online' or 'Offline'")
        else:
            room = self.get_chatroom(room_name=room_name)
            if username == room.from_user.username:
                room.from_user_status = True if status == 'Online' else False
            elif username == room.to_user.username:
                room.to_user_status = True if status == 'Online' else False
            else:
                raise ValueError("User is not in this chatroom")
            room.save()



    def create(self, from_username, to_username):
        return self.create_chatroom(from_username, to_username)


class ChatMessageManager(models.Manager):
    def create_message(self, chat_room, sent_by, message_string=None, error=None):
        if not message_string and not error:
            raise ValueError("Message string and error string cannot be both None!")
        elif not sent_by and sent_by != '' and chat_room.from_user.username != sent_by and chat_room.to_user.username != sent_by:
            raise ValueError("Message cannot send to others\' chatroom")
        else:
            if error:
                status = 'err'
            elif message_string:
                status = 'msg'
            new_msg = self.model(
                chat_room = chat_room,
                message_string = message_string,
                message_status = status,
                sent_by = sent_by
            )
            new_msg.save()
            return new_msg
    
    def delete_message(self, message_id):
        if not message_id:
            raise ValueError("Chat Message cannot be empty")
        else:
            return self.get_queryset().filter(id=message_id).update(message_status='spc', message_string='This message has been deleted.')
    
    def forward_message(self, from_username, to_username, message_id):
        if not from_username or not to_username or not message_id:
            raise ValueError("Both usernames and the message ID cannot be empty")
        else:
            msg = self.get_queryset().get(id=message_id)
            from_room = msg.chat_room
            if from_room.from_user.username != from_username and from_room.to_user.username != from_username:
                raise ValueError("Cannot forward message in others\' room")
            elif from_room.from_user.username == to_username or from_room.to_user.username == to_username:
                raise ValueError("Cannot forward message to the same room")
            else:
                try:
                    to_room = ChatRoom.objects.get_chatroom(from_username=from_username, to_username=to_username)
                except:
                    to_room = ChatRoom.objects.create_chatroom(from_username, to_username)
                return self.create_message(to_room, from_username, msg.message_string)

    def get_message_count(self, room_name=None, from_username=None, to_username=None):
        return len(self.get_messages_from_chatroom(room_name, from_username, to_username))
    
    def get_messages_from_chatroom(self, room_name=None, from_username=None, to_username=None, count=0):
        if (not room_name and (not from_username or not to_username)):
            raise ValueError("Room Name and either username cannot be None together")
        elif room_name:
            chat_room = ChatRoom.objects.get_chatroom(room_name)
        else:
            chat_room = ChatRoom.objects.get_chatroom(from_username=from_username, to_username=to_username)
        if count == 0: return self.get_queryset().filter(models.Q(chat_room=chat_room))
        else: return self.get_queryset().filter(models.Q(chat_room=chat_room))[:count]

class ChatRoom(models.Model):
    room_name = models.AutoField(primary_key=True)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user_set', on_delete=models.CASCADE)
    from_user_status = models.BooleanField(default=False)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user_set' ,on_delete=models.CASCADE)
    to_user_status = models.BooleanField(default=False)

    objects = ChatRoomManager()

    def __str__(self):
        return str(self.room_name)

class ChatMessage(models.Model):
    STATUS_CHOICES = [
        ('msg', 'Chat_Message'),
        ('err', 'Chat_Error'),
        ('spc', 'Chat_Special')
    ]

    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    message_string = models.CharField(max_length=255, blank=True)
    message_status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='msg')
    error = models.CharField(max_length=255, blank=True)
    sent_by = models.CharField(max_length=255, default='')
    sent_time = models.DateTimeField(auto_now_add=True)

    objects = ChatMessageManager()

    def __str__(self):
        return self.message_string

    class Meta:
        ordering = ["sent_time"]


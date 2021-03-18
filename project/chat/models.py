from django.db import models

class ChatRoomManager(models.Manager):
    def get_chatroom(self, room_name=None,from_user=None, to_user=None, exact=False):
        if (not room_name and (not from_user or not to_user)):
            raise ValueError("Room Name and either username cannot be None together")
        elif room_name:
            return self.get_queryset().get(room_name=room_name)
        else:
            if not exact:
                room = self.get_all_chatrooms_by_user(from_user, self.get_all_chatrooms_by_user(to_user))
                if len(room) == 0:
                    raise models.ObjectDoesNotExist
                elif len(room) > 1:
                    raise models.MultipleObjectsReturned
                else:
                    return room[0]
            else:
                return self.get_queryset().get(from_user=from_user, to_user=to_user)
    
    def get_all_chatrooms_by_user(self, from_user, query=None):
        if not query:
            return self.get_queryset().filter(models.Q(from_user=from_user) | models.Q(to_user=from_user))
        else:
            return query.filter(models.Q(from_user=from_user) | models.Q(to_user=from_user))

    def create_chatroom(self, from_user, to_user):
        if from_user == "" or to_user == "" or from_user == to_user:
            raise ValueError("Chat Room must have two unique users")
        else:
            try:
                room = self.get_chatroom(from_user=from_user, to_user=to_user)
                return room
            except models.MultipleObjectsReturned:
                raise ValueError("Duplicated Chatrooms found, need to fix before creating new chatroom")
            except:
                new_room = self.model(
                    from_user=from_user,
                    to_user=to_user
                )
                new_room.save()
                return new_room

    def create(self, from_user, to_user):
        return self.create_chatroom(from_user, to_user)


class ChatMessageManager(models.Manager):
    def create_message(self, chat_room, sent_by, message_string=None, error=None):
        if not message_string and not error:
            raise ValueError("Message string and error string cannot be both None!")
        elif not sent_by and sent_by != '' and chat_room.from_user != sent_by and chat_room.to_user != sent_by:
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
    
    def forward_message(self, from_user, to_user, message_id):
        if not from_user or not to_user or not message_id:
            raise ValueError("Both users and the message ID cannot be empty")
        else:
            msg = self.get_queryset().get(id=message_id)
            from_room = msg.chat_room
            if from_room.from_user != from_user and from_room.to_user != from_user:
                raise ValueError("Cannot forward message in others\' room")
            elif from_room.from_user == to_user or from_room.to_user == to_user:
                raise ValueError("Cannot forward message to the same room")
            else:
                try:
                    to_room = ChatRoom.objects.get_chatroom(from_user=from_user, to_user=to_user)
                except:
                    to_room = ChatRoom.objects.create_chatroom(from_user, to_user)
                return self.create_message(to_room, from_user, msg.message_string)


    def get_message_count(self, room_name=None, from_user=None, to_user=None):
        return len(self.get_messages_from_chatroom(room_name, from_user, to_user))
    
    def get_messages_from_chatroom(self, room_name=None, from_user=None, to_user=None):
        if (not room_name and (not from_user or not to_user)):
            raise ValueError("Room Name and either username cannot be None together")
        elif room_name:
            chat_room = ChatRoom.objects.get_chatroom(room_name)
        else:
            chat_room = ChatRoom.objects.get_chatroom(from_user=from_user, to_user=to_user)
        return self.get_queryset().filter(models.Q(chat_room=chat_room))


class ChatRoom(models.Model):
    room_name = models.AutoField(primary_key=True)
    from_user = models.CharField(max_length=255)
    to_user = models.CharField(max_length=255)

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


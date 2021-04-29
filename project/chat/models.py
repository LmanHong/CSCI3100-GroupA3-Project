from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class ChatRoomManager(models.Manager):
#Functions for manipulating chatroom instances
    def get_chatroom(self, room_name=None,from_username=None, to_username=None, exact=False):
        #Get chatroom by either the room name or by a pair of username
        if (not room_name and (not from_username or not to_username)):
            raise ValueError("Room Name and either username cannot be None together")
        elif room_name:
            #Get chatroom by room name
            return self.get_queryset().get(room_name=room_name)
        else:
            #Get user instances from usernames
            from_user = get_user_model().objects.get(username=from_username)
            to_user = get_user_model().objects.get(username=to_username)
            if not exact:
                #Get chatroom that contains both users
                rooms = self.get_queryset().filter((models.Q(from_user=from_user) & models.Q(to_user=to_user)) | (models.Q(from_user=to_user) & models.Q(to_user=from_user)))
                if len(rooms) == 0:
                    raise ObjectDoesNotExist
                elif len(rooms) > 1:
                    raise MultipleObjectsReturned
                else:
                    return rooms[0]
            else:
                #If exact is true, meaning the position of from_user and to_user is exact and not swapped
                return self.get_queryset().get(from_user=from_user, to_user=to_user)
    
    def get_all_chatrooms_by_user(self, from_username, query=None):
        #Get all chatroom that has the user in it
        if not from_username:
            raise ValueError("username cannot be None")
        else:
            #Get the user instance
            from_user = get_user_model().objects.get(username=from_username)
            if not query:
                return self.get_queryset().filter(models.Q(from_user=from_user) | models.Q(to_user=from_user))
            else:
                #If a list of chatrooms is provided, search only in that list
                return query.filter(models.Q(from_user=from_user) | models.Q(to_user=from_user))

    def create_chatroom(self, from_username, to_username):
        #Create a new chatroom between the two given users if not exists
        if from_username == "" or to_username == "" or from_username == to_username:
            raise ValueError("Chat Room must have two unique and non-empty usernames")
        else:
            #Get the user instances
            from_user = get_user_model().objects.get(username=from_username)
            to_user = get_user_model().objects.get(username=to_username)
            try:
                #If a chatroom between the two users already exist, return the chatroom instead
                room = self.get_chatroom(from_username=from_username, to_username=to_username)
                return room
            except MultipleObjectsReturned:
                raise ValueError("Duplicated Chatrooms found, need to fix before creating new chatroom")
            except:
                #Create a new chatroom and return it if not exists
                new_room = self.model(
                    from_user=from_user,
                    to_user=to_user
                )
                new_room.save()
                return new_room

    def set_online_status(self, room_name, username, status):
        #Set the online status of the given user in a chatroom
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
        #Alias of create_chatroom 
        return self.create_chatroom(from_username, to_username)


class ChatMessageManager(models.Manager):
#Functions for manipulating chat messages
    def create_message(self, chat_room, sent_by, message_string=None, error=None):
        #create a new chat message in the chat room
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
        #Delete the chat message with the message_id
        if not message_id:
            raise ValueError("Chat Message cannot be empty")
        else:
            return self.get_queryset().filter(id=message_id).update(message_status='spc', message_string='This message has been deleted.')
    
    def forward_message(self, from_username, to_username, message_id):
        #Forward the chat message with message_id to another user
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
                #If the message can be forwarded to the target user, create a copied message in the destinated chat room 
                try:
                    to_room = ChatRoom.objects.get_chatroom(from_username=from_username, to_username=to_username)
                except:
                    to_room = ChatRoom.objects.create_chatroom(from_username, to_username)
                return self.create_message(to_room, from_username, msg.message_string)

    def get_message_count(self, room_name=None, from_username=None, to_username=None):
        #Get the mesage count of a given chatroom
        return len(self.get_messages_from_chatroom(room_name, from_username, to_username))
    
    def get_messages_from_chatroom(self, room_name=None, from_username=None, to_username=None, count=0):
        #Get chat messages from a chatroom
        if (not room_name and (not from_username or not to_username)):
            raise ValueError("Room Name and either username cannot be None together")
        elif room_name:
            chat_room = ChatRoom.objects.get_chatroom(room_name)
        else:
            chat_room = ChatRoom.objects.get_chatroom(from_username=from_username, to_username=to_username)
        #If no message count is set, return all messages, else return the specified number of messages
        if count == 0: return self.get_queryset().filter(models.Q(chat_room=chat_room))
        else: return self.get_queryset().filter(models.Q(chat_room=chat_room))[:count]
    
    def get_latest_message(self, room_name=None, from_username=None, to_username=None):
        #Get the last message of a chatroom
        try:
            latest_msg = self.get_messages_from_chatroom(room_name=room_name,  from_username=from_username, to_username=to_username)
            return latest_msg[len(latest_msg)-1]
        except:
            return None

class ChatRoom(models.Model):
    #Model (Schema) of the chatroom instance
    room_name = models.AutoField(primary_key=True)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user_set', on_delete=models.CASCADE) #User instance of the room initiating user
    from_user_status = models.BooleanField(default=False) #Initiaing user's online status
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user_set' ,on_delete=models.CASCADE) #User instance of the targeted user
    to_user_status = models.BooleanField(default=False) #Targeted user's online status

    objects = ChatRoomManager()

    def __str__(self):
        return str(self.room_name)

class ChatMessage(models.Model):
    #Model (Schema) of the chat message
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

@receiver(post_save, sender=ChatMessage)
def broadcast_latest_msg(sender, instance, created, **kwargs):
    #Broadcast the latest message notification to both the sender and the receiver 
    if created:
        print("New chat message created. ", instance)
        chat_room = instance.chat_room
        sent_by = instance.sent_by
        from_user = chat_room.from_user
        to_user = chat_room.to_user
        sent_to = from_user.username if sent_by == to_user.username else to_user.username
        print(sent_by, sent_to)

        #Get the notification group names of both users
        noti_group1 = "notification_{}".format(sent_by.replace(" ", ""))
        noti_group2 = "notification_{}".format(sent_to.replace(" ", ""))

        #Send the notification to the groups
        async_to_sync(get_channel_layer().group_send)(
            noti_group1,
            {
                'type': 'latestMsg',
                'latest_msg':{
                    'message_string': instance.message_string,
                    'sent_by': sent_by,
                    'sent_to': sent_to
                }
            }
        )
        async_to_sync(get_channel_layer().group_send)(
            noti_group2,
            {
                'type': 'latestMsg',
                'latest_msg':{
                    'message_string': instance.message_string,
                    'sent_by': sent_by,
                    'sent_to': sent_to
                }
            }
        )


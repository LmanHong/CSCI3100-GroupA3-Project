from django.db import models
from django.models import manager

class FrdSearchManager(models.manager):
    #check whether the input is empty
    def checkinput(self,college,study_field,hobbies,gender,behavior):
        if not college and not study_field and not hobbies and not gender and not behavior:
            raise ValueError("At least one of the row must be filled")
        #...

class FriendList(models.Model):
    user1 = models.CharField(max_length=32)
    user2 = models.CharField(max_length=32)

    def createFrdList(self, user1, user2):
        # store the link of them into database if user accept

from django.db import models
from django.conf import settings

class FrdSearchManager(models.manager):
    #check whether the input is empty
    def checkinput(self,college,study_field,hobbies,gender,behavior,from_user):
        if not college and not study_field and not hobbies and not gender and not behavior:
            raise ValueError("At least one of the row must be filled")
        else:
            return True
    
    def SearchFrd(self,college,study_field,hobbies,gender,behavior,from_user):
        if checkinput(college,study_field,hobbies,gender,behavior,from_user):
            #find the perfered friend
            #if there is no friend on the result of the query
            #raise ValueError("No result")
            #else print the output from the query



#to link the users(to match them)
class FriendLink(models.Model):
    def sendRequest(self,from_user, to_user):
        #send the request(approval for making friend) to to_user

    def createFrdList(self, from_user, to_user):
        # store the link of them into database if user accept
        if from_user == "" or to_user == "" or from_user == to_user:
            raise ValueError("The users' name cannot be null or same")
    
    def isAlreadyFrdList(self, from_user, to_user):
        pass
    #if from_user and to_user already are already being friends:
    #raise ValueError("Already made!")
    #else: return false


#the database to store the friend list
class FriendList(models,Model):
    linkID = models.IntegerField(primary_key=True)
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user1,self.user2



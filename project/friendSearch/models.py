from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
#from account.models import profile

class FriendListManager(models.Manager):
    def checkinput(self,user,gender,jobtitles,passions):
        if not user or not jobtitles or not passions or not gender:
            raise ValueError("All rows cannot be empty")
        else:
            return True

    #put in view.py 
    def SearchFrd(self,user,gender,jobtitles,passions):
        if checkinput(user,gender,jobtitles,passions):
            joblist = jobtitles.split(" ")
            query1 = [models.Q(jobtitles__icontains=job) for job in joblist]
            jobquery = models.Q()
            for item in query1:
                jobquery &= item
            passionlist = passions.split(" ")
            query2 = [models.Q(passions__icontains=passion) for passion in passionlist]
            passionquery = models.Q()
            for item in query2:
                passionquery &= item
            if gender != "any":
                results = profile.objects.filter(jobquery).filter(passionquery).filter(gender=gender) #to get the potential friend
            else:
                results = profile.objects.filter(jobquery).filter(passionquery)
            result = results.exclude(user=user).values_list('user')
        return results

    def createFrdList(self, from_username, to_username):
        # store the link of them into database if user accept
        if from_username == "" or to_username == "" or from_username == to_username:
            raise ValueError("The users' name cannot be null or same")
        elif not isAlreadyFrdList(from_username,to_username):
            from_user = get_user_model.objects.get(username=from_username)
            to_user = get_user_model.objects.get(username=to_username)
            friendship = self.models(
                user = from_user,
                friend = to_user,
                status = 'acp'
            )
            friendship2 = self.models(
                user = to_user,
                friend = from_user,
                status = 'acp'
            )
            friendship.save()
            friendship2.save()
            return friendship
        else:
            raise ValueError("The user you selected is already your friend")
        
    def isAlreadyFrdList(self, from_user, to_user):
        friend = FriendList.object('friend').filter(user=from_user,friend=to_user)
        if len(friend) >= 1:
            return False
        return True


class RequestsManager(models.Manager):
    def createRequest(self,from_username, to_username):
        if from_username == to_username or from_username == "" or to_username == "":
            print("the name ofuser and friend cannot be null or same")
        else:
            from_user = get_user_model.objects.get(username=from_username)
            to_user = get_user_model.objects.get(username=to_username)
            request = self.models(
                user = from_user,
                receiver = to_user
            )
            request.save()
            return request
    
    def handleRequest(self, from_user, to_user, option):
        #

class FriendList(models.Model):

    Link_Choice = [
        ('acp', 'accept'),
        ('rej', 'reject'),
        ('unk', 'unknown'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user', on_delete=models.CASCADE)
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='friend', on_delete=models.CASCADE)
    status = models.CharField(max_length=3, default='unk') #accept or reject

    objects = FriendListManager()

    def __str__(self):
        return self.user1, self.friend

    class Meta:
        ordering = ['user']

#class profile(models.Model):


class Requests(models.Model): #to store the request to a user from a user
    Status_Choice = [
        ('Y','seen'),
        ('N','not seen')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='friend', on_delete=models.CASCADE)
    status  = models.CharField(max_length=1, default='N')

    objects = RequestsManager()

    def __str__(self):
        return self.user, self.receiver
    
    class Meta:
        ordering = ['user']

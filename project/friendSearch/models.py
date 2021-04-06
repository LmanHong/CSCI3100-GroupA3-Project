from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from account.models import Profile, Account
#prototype only

class FriendListManager(models.Manager):
    def checkinput(self,user,gender,jobtitles,passions):
        if not user or not jobtitles or not passions or not gender:
            raise ValueError("All rows cannot be empty")
        else:
            return True

    #to serch friend base on their perference, to return the fulfilled query except user and user's friend
    def SearchFrd(self,user,gender,jobtitles,passions):
        if self.checkinput(user,gender,jobtitles,passions):
            joblist = jobtitles.split(", ")
            query1 = [models.Q(job_title__icontains=job) for job in joblist]
            jobquery = models.Q()
            for item in query1:
                jobquery &= item
            passionlist = passions.split(", ")
            query2 = [models.Q(passions__icontains=passion) for passion in passionlist]
            passionquery = models.Q()
            for item in query2:
                passionquery &= item
            if gender != "any":
                results = Profile.objects.filter(jobquery).filter(passionquery).filter(gender=gender) #to get the potential friend
            else:
                results = Profile.objects.filter(jobquery).filter(passionquery)
            friend_of_user = FriendList.objects.returnFriendID(user)
            #print(friend_of_user)
            result = list(results.exclude(user=user).exclude(user__in = friend_of_user).values_list('user_id',flat=True)) #the result
            nlist = Account.objects.select_related('id').filter(id__in = result).values('username','id')
            #print(nlist)
        return nlist

    #to make friend link between user and friend
    def createFrdList(self, from_user, to_username):
        # store the link of them into database if user accept
        to_user = get_user_model().objects.get(username=to_username)
        existThatRequest = Requests.objects.filter(models.Q(sender = to_user,receiver = from_user,status="N"))
        if not existThatRequest:
            raise ValueError("There is no request made by {}".format(from_user))
        elif not FriendList.objects.isAlreadyFrdList(from_user,to_user):
            friendship = self.model(
                user = from_user,
                friend = to_user,
                status = 'acp'
            )
            friendship.save()
            friendship2 = self.model(
                user = to_user,
                friend = from_user,
                status = 'acp'
            )
            friendship2.save()
            Requests.objects.filter(models.Q(sender = to_user, receiver = from_user, status="N") | models.Q(sender = from_user, receiver = to_user, status="N")).update(status="Y")
            return friendship
        else:
            raise ValueError("{} is already your friend".format(to_user))

    #to check if the to_user is a friend to user
    def isAlreadyFrdList(self, from_user, to_username):
        try:
            to_user = get_user_model().objects.get(username=to_username)
            friend = FriendList.object('friend').filter(user=from_user,friend=to_user)
            if len(friend) >= 1:
                return False
            return True
        except:
            print("DNE")
            return False
    
    #to return the result of query of friend
    def returnFriendList(self, user):
        friend_id_list = list(FriendList.objects.filter(models.Q(user=user)).values_list('friend',flat=True))
        #print(friend_id_list)
        nlist = Account.objects.select_related('id').filter(id__in = friend_id_list).values('username','id')
        #print(nlist)
        return nlist
    #to return the foeign key(the friend.id)
    def returnFriendID(self,user):
        friend_id_list = list(FriendList.objects.filter(models.Q(user=user)).values_list('friend',flat=True))
        nlist = list(Account.objects.select_related('id').filter(id__in = friend_id_list).values_list('id',flat=True))
        return nlist

class RequestsManager(models.Manager):
    #to make and send request to the user
    def createRequest(self,from_user, to_username):
        to_user = get_user_model().objects.get(username=to_username) #flow objectdoesnotexist exception
        existThatRequest = Requests.objects.filter(models.Q(sender = from_user,receiver = to_user,status="N"))
        if existThatRequest:
            raise ValueError("You have already sent requests to {}".format(to_username))
        else:
            request = self.model(
                sender = from_user,
                receiver = to_user,
                status = 'N'
            )
            request.save()
            return request

    #to handle the request--> make friend
    def handleRequest(self, to_user, from_user):
        if from_user == to_user or from_user == "" or to_user == "":
            print("the name ofuser and friend cannot be null or same")
        else:
            Requests.objects.filter(sender = from_user, receiver=to_user).update(status = 'Y')
            friendship = FriendList.objects.createFrdList(to_user, from_user)
            return friendship

    #to return the request the user receive
    def returnRequest(self, user): #can be viewed in the request_list.html
        result = list(Requests.objects.filter(models.Q(receiver = user, status = "N")).values_list('sender', flat=True)) #the user id 
        namelist = Account.objects.select_related('id').filter(id__in = result).values('username','id')
        return namelist
    
    #to reject the request
    def rejectRequest(self, user, sendername):
        sender = get_user_model().objects.get(username=sendername)
        existThatRequest = Requests.objects.filter(models.Q(sender = sender,receiver = user,status="N"))
        if not sender:
            raise ValueError("{} doesn't exist.")
        elif not existThatRequest:
            raise ValueError("There is no request made by {}.".format(sendername))
        else:
            Requests.objects.filter(sender = sender, receiver=user).delete()
            
#basic data structure of models            
class FriendList(models.Model):
 
    Link_Choice = [
        ('acp', 'accept'),
        ('rej', 'reject'),
        ('unk', 'unknown'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user', on_delete=models.CASCADE)
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='friend', on_delete=models.CASCADE)
    status = models.CharField(max_length=3, choices = Link_Choice, default='unk') #accept or reject

    objects = FriendListManager()

    def __str__(self):
        return self.user1, self.friend

    class Meta:
        ordering = ['user']



class Requests(models.Model): #to store the request to a user from a user
    Status_Choice = [
        ('Y','seen'),
        ('N','not seen')
    ]
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='receiver', on_delete=models.CASCADE)
    status  = models.CharField(max_length=1, choices = Status_Choice, default='N')

    objects = RequestsManager()

    def __str__(self):
        return self.user, self.receiver
    
    class Meta:
        ordering = ['sender']

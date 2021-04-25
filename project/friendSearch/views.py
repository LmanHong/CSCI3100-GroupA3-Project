from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate, logout
from friendSearch.forms import SearchForm, RequestForm
from django.contrib import messages
from django.http import HttpResponse
from .models import Requests, FriendList
from django.core.exceptions import ObjectDoesNotExist

#view for friendSearchView
class FriendSearchView(View):
    #to get the view of friendSearch
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            context = {}
            context['SearchForm'] = SearchForm()
            return render(request,'frd_searching.html',context)
        else:
            print('You are not logging in')
            return redirect('login')

    #to receive the information from form and send it to search_result.html
    def post(self, request, *args, **kwargs):
        user = request.user
        context = {}
        #a form to store search query
        fform = SearchForm(request.POST or None)
        # a form to store input line
        form = RequestForm(request.POST or None)
        if not user.is_authenticated:
            return redirect('login')
        if fform.is_valid(): #for search query part
            #take the information from the form
            gender = request.POST['gender']
            jobtitle = request.POST['jobtitle']
            passion = request.POST['passions']
            friendlist = FriendList.objects.SearchFrd(user,gender,jobtitle,passion)
            context['frdlist'] = friendlist
            context['RequestForm'] = RequestForm()
            #print(context['frdlist'])
            return render(request,'search_result.html',context)
        elif form.is_valid(): #for input line to send request part
            lists = request.POST['usernamelist']
            friendlist = lists.split(", ") 
            modifiedlist = [name for name in friendlist if name != ""]
            if(len(modifiedlist)==0):
                messages.error(request,"The input is valid")
                return render(request,'search_result.html',context)
            else:
                for to_user_name in modifiedlist:
                    try:
                        Requests.objects.createRequest(user,to_user_name)
                        messages.info(request,"request to {} is sent".format(to_user_name))
                        print("request to {} is sent".format(to_user_name))
                    except ValueError as e:
                        messages.error(request,e)
                        print(e)
                    except ObjectDoesNotExist as e:
                        messages.error(request,"{} does not exist".format(to_user_name))
                        print("{} does not exist".format(to_user_name))
                #redirect after sending all requests
                return redirect('friendSearch')
        else:
            context['SearchForm'] = fform
            return render(request,'search_result.html', context)
        #to get the information of the form and send to the dbs

#class FriendListView(View):
#    def get(self, request, *args, **kwargs): #to return the list of the friend
#        user = request.user
#        context = {}
#
#        if user.is_authenticated:        
#            friendlist = FriendList.objects.returnFriendList(user)
#            context['friendlist'] = friendlist
#            return render(request,'frd_list.html',context)
#        else:
#            return redirect('home')
#    
#    def post(self, request, *args, **kwargs): #for chatting?
#        #to check if the user click accept or reject --> if yes: add to frdlist (storing in dbs)
#        context = {}
#        user = request.user
#        form = RequestForm(request.POST)
#        if user.is_authenticated and form.is_valid():
#            lists = request.POST['usernamelist']
#            #print("as",lists)
#            context['successful'] = "Request is sent"
#            return render(request,'frd_list.html',context)
#        else:
#            return redirect('home')

#the view for request page
class RequestView(View):
    # to get view of request page
    def get(self, request, *args, **kwargs):
        user = request.user
        context = {}
        # a form to store the input line
        context['approvelist'] = RequestForm()

        if user.is_authenticated:        
            requested_by_users = Requests.objects.returnRequest(user)
            context['requestlist'] = requested_by_users
            return render(request,'requests_list.html', context)
        else:
            return redirect('login')

    #to receive the information for request page
    def post(self, request, *args, **kwargs):
        user = request.user
        form = RequestForm(request.POST)
        if not user.is_authenticated:
            return redirect('login')
        if form.is_valid():
            lists = request.POST['usernamelist']
            userlist = lists.split(", ")
            modifiedlist = [name for name in userlist if name != ""]
            if(len(modifiedlist)==0):
                messages.error(request,"Invalid Input")
                return redirect('request')
            else:
                for to_user_name in modifiedlist:
                    try:
                        FriendList.objects.createFrdList(user,to_user_name)
                        messages.info(request,"friend to {} is made".format(to_user_name))
                    except ValueError as e:
                        messages.error(request,e)
                    except ObjectDoesNotExist as e:
                        messages.error(request,"{} does not exist".format(to_user_name))
                return redirect('request')
        else:
            return redirect('request')


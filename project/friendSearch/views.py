from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate, logout
from friendSearch.forms import SearchForm
from django.http import HttpResponse
from .models import Requests, FriendList

class FriendSearchView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            context = {}
            context['SearchForm'] = SearchForm()
            return render(request,'frd_searching.html',context)
        else:
            print('You are not logging in')
            return redirect('home')
    
    def post(self, request, *args, **kwargs):
        user = request.user
        context = {}
        fform = SearchForm(request.POST or None)
        if fform.is_valid():
            gender = request.POST['gender']
            jobtitle = request.POST['jobtitle']
            passion = request.POST['passions']
            friendlist = FriendList.objects.SearchFrd(user,gender,jobtitle,passion)
            context['frdlist'] = friendlist
            #print(context['frdlist'])
            return render(request,'frd_list.html',context)
        else:
            context['SearchForm'] = fform
            return render(request,'frd_list.html',context)
        #to get the information of the form and send to the dbs

class FriendList(view):
    def get(self,request):
        return render(request,'template/frd_list',{})
    
    def post(self,request):
        #to check if the user click accept or reject --> if yes: add to frdlist (storing in dbs)



# Create your views here.

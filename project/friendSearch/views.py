from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse

class FriendSearch(view):
    def get(self,request):
        return render(request,'template/frd_searching',{})
    
    def post(self,request):
        pass
        #to get the information of the form and send to the dbs

class FriendList(view):
    def get(self,request):
        return render(request,'template/frd_list',{})
    
    def post(self,request):
        #to check if the user click accept or reject --> if yes: add to frdlist (storing in dbs)



# Create your views here.

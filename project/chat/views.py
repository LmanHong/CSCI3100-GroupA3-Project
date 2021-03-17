from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

def chat_room(request):
    return render(request, 'chat/index.html')


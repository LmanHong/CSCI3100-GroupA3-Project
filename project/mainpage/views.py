from django.shortcuts import render

from django.views import View
from django.http import HttpResponse

def main_page(request):
    return render(request, 'mainpage/index.html')

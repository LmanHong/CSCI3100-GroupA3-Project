from django.shortcuts import render

from django.views import View
from django.http import HttpResponse

class main_page(View):
    def get(self,request):
        return render(request,'index.html')

#def main_page(request):
 #   return render(request, 'mainpage/index.html')

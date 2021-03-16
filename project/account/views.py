from django.shortcuts import render, redirect
from django.views import View

class HomeView(View):
    def get(self, request):
        return redirect('profile')

class ProfileView(View):
    def get(self, request):
        return render(request, 'profile.html', {})
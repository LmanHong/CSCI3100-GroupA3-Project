from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm

class HomeView(View):
    def get(self, request):
        return redirect('profile')

class ProfileView(View):
    def get(self, request):
        return render(request, 'profile.html', {})

class RegistrationView(View):
    def get(self, request):
        context = {}
        form = RegistrationForm()
        context['registration_form'] = form
        return render(request, 'register.html', context)
    
    def post(self, request):
        context = {}
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form
            return render(request, 'register.html', context)
            
def logout_view(request):
    logout(request)
    return redirect('home')
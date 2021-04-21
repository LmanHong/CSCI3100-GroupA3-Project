from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from account.forms import RegistrationForm, AccountAuthenticationForm, ProfileUpdateForm
from django.http import HttpResponseRedirect


class HomeView(View):
    def get(self, request):
        return redirect('profile')

class ProfileView(View):
    def get(self, request):
        return render(request, 'profile.html', {})

class RegistrationView(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return redirect('profile')
        else:
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
            return redirect('profile')
        else:
            context['registration_form'] = form
            return render(request, 'register.html', context)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')

class LoginView(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            next_url = request.GET.get('next')
            if next_url:
                return HttpResponseRedirect(next_url)
            else:
                return redirect('profile')
        else:
            context = {}
            form = AccountAuthenticationForm()
            context['login_form'] = form
            return render(request, 'login.html', context)

    def post(self, request):
        context = {}
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                next_url = request.POST.get('next')
                if next_url:
                    return HttpResponseRedirect(next_url)
                else:
                    return redirect('profile')
            else:
                context['login_form'] = form
                return render(request, 'login.html', context)
        else:
            context['login_form'] = form
            return render(request, 'login.html', context)

@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    context = {}
    context['profile_update_form'] = form

    return render(request, 'profile_update.html', context)
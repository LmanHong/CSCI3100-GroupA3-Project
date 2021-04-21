from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from account.forms import RegistrationForm, AccountAuthenticationForm, ProfileUpdateForm
from django.http import HttpResponseRedirect

# view for profile page
class HomeView(View):
    def get(self, request):
        return redirect('profile')

# view for profile page
class ProfileView(View):
    def get(self, request):
        return render(request, 'profile.html', {})

# view for registration page
class RegistrationView(View):
    def get(self, request):
        user = request.user
        # if the user is already logged in
        if user.is_authenticated:
            return redirect('profile')
        # if the uesr is not logged in, send the registration form
        else:
            context = {}
            form = RegistrationForm()
            context['registration_form'] = form
            return render(request, 'register.html', context)
    
    # submit the registration form
    def post(self, request):
        context = {}
        form = RegistrationForm(request.POST)
        # if the form is valid in format
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            # login the account
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('profile')
        # if the form is invalid in format
        else:
            context['registration_form'] = form
            return render(request, 'register.html', context)

# view for logout page
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')

# view for login page
class LoginView(View):
    def get(self, request):
        user = request.user
        # if the user is already logged in, redirect them to the appropriate page
        if user.is_authenticated:
            next_url = request.GET.get('next')
            if next_url:
                return HttpResponseRedirect(next_url)
            else:
                return redirect('profile')
        # if the user is not logged in, send the login form
        else:
            context = {}
            form = AccountAuthenticationForm()
            context['login_form'] = form
            return render(request, 'login.html', context)

    # submit the login form
    def post(self, request):
        context = {}
        form = AccountAuthenticationForm(request.POST)
        # if the form is valid in format
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            # if the user email and password is correct
            if user:
                login(request, user)
                # redirect user to the appropriate page
                next_url = request.POST.get('next')
                if next_url:
                    return HttpResponseRedirect(next_url)
                else:
                    return redirect('profile')
            # if the user email and password is incorrect
            else:
                context['login_form'] = form
                return render(request, 'login.html', context)
        # if the form is invalid in format
        else:
            context['login_form'] = form
            return render(request, 'login.html', context)

# view for profile update page
@login_required
def profile_update(request):
    # submit the profile update form
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            # redirect user to the appropriate page
            return redirect('profile')
    # get the profile update form
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    context = {}
    context['profile_update_form'] = form

    # show the form
    return render(request, 'profile_update.html', context)
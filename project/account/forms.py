from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import Account, Profile

# account registration
class RegistrationForm(UserCreationForm):
    # additional information for the field
    email = forms.EmailField(max_length=64, help_text='A valid email address')

    class Meta:
        model = Account
        # required fields
        fields = ('email', 'username', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        # add classes to the fields so that the style can be changed easily
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class AccountAuthenticationForm(forms.ModelForm):
    # additional information for the field
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        # required fields
        fields = ('email', 'password')
    
    def clean(self):
        # log in the user if the fields are correct
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid login')
    
    def __init__(self, *args, **kwargs):
        super(AccountAuthenticationForm, self).__init__(*args, **kwargs)
        # add classes to the fields so that the style can be changed easily
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        # required fields
        fields = ('image', 'first_name', 'last_name', 'gender', 'date_of_birth', 'job_title', 'passions')
    
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        # add classes to the fields so that the style can be changed easily
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
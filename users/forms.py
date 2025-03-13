from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

#The user registration form class inherits from Django
class UserRegisterForm(UserCreationForm):
    #Email field: Django field has only username and password by default
    email = forms.EmailField()

    #Define a nested Meta class to configure the behavior of the user model
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

#User update personal information form
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

#User Profile Update Form
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']
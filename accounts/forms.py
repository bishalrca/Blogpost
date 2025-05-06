# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'profile_picture', 'password1', 'password2']

class ProfileUpdateForm(UserChangeForm):
    # username=forms.CharField(max_length=10)
    # email = forms.EmailField( required=False)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'profile_picture']
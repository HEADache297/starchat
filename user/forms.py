from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.forms.widgets import Input, EmailInput, PasswordInput

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=255, required=True, widget=EmailInput(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-white text-black', 'placeholder': 'Email'}))
    username = forms.CharField(max_length=255, required=True, widget=Input(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-white text-black', 'placeholder': 'Username'}))
    password1 = forms.CharField(widget=PasswordInput(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-white text-black', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-white text-black', 'placeholder': 'Password Confirmation'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=255, widget=Input(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-white text-black', 'placeholder': 'Username'}))
    password = forms.CharField(max_length=255, widget=PasswordInput(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-white text-black', 'placeholder': 'Email'}))
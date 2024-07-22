from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,SetPasswordForm,PasswordResetForm
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
    password = forms.CharField(max_length=255, widget=PasswordInput(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-white text-black', 'placeholder': 'Password'}))



class ChangeImageForm(forms.Form):
    image = forms.ImageField()


class UpdatePasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-white text-black', 'placeholder': 'Password', 'id': 'inp1'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-white text-black', 'placeholder': 'Password Confirmation', 'id': 'inp2'}))

    def __init__(self, *args, **kwargs):
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].label = ""
        self.fields['new_password2'].label = ""

    class Meta:
        model=User
        fields= ['new_password1', 'new_password2']

class ResetPasswordForm(PasswordResetForm):
    username=forms.CharField(required=True, min_length=3, widget=Input(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-white text-black', 'placeholder': 'Username', 'id': 'inp1'}))
    email=forms.EmailField(required=True, widget=EmailInput(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-white text-black', 'placeholder': 'Email', 'id': 'inp2'}))
    
    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = ""
        self.fields['email'].label = ""
    class Meta:
        model=User
        fields= ['username', 'email']
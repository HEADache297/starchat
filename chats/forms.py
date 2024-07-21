from django.forms import ModelForm
from django import forms
from .models import Messages

class MessagesForm(forms.ModelForm):
    
    class Meta:
        model = Messages
        fields = ['content']
        widgets = {
            'content' : forms.TextInput(attrs={'placeholder' : 'Type a message...', 'class' : 'flex-grow shadow-lg border rounded-l-lg p-2 outline-none'})
        }
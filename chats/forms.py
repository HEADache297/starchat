from django.forms import ModelForm
from django import forms
from .models import Messages

class MessagesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MessagesForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = ""

    class Meta:
        model = Messages
        fields = ['content']
        widgets = {
            'content' : forms.TextInput(attrs={'label': ' ', 'placeholder' : 'Type a message...', 'class' : 'w-full border-r-0 flex-grow shadow-lg border rounded-l-lg p-2 outline-none', 'id': 'inputt'})
        }
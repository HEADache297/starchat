from django.forms import ModelForm
from django import forms
from .models import Messages

class MessagesForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'w-full border-y-[1px] p-1 h-full hidden'}))

    def __init__(self, *args, **kwargs):
        super(MessagesForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = ""
        self.fields['image'].label = ""

    class Meta:
        model = Messages
        fields = ['content', 'image']
        widgets = {
            'content' : forms.TextInput(attrs={'label': ' ', 'placeholder' : 'Type a message...', 'class' : 'w-full border-r-0 flex-grow shadow-lg border rounded-l-lg p-2 outline-none', 'id': 'inputt'})
        }
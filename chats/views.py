from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import ChatRoom, Messages
from .forms import MessagesForm
# Create your views here.

@login_required
def chat_view(request):
    chat_room = get_object_or_404(ChatRoom)
    chat_messages = chat_room.chat_messages.all()[:30]
    
    form = MessagesForm()
    
    if request.method == 'POST':
        form = MessagesForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.chat = chat_room
            message.save()
            print('message create')
        else:
            form = MessagesForm()
            
    return render(request, 'core/chats.html', {'chat_messages' : chat_messages, 'chat_room' : chat_room, 'form' : form})
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import ChatRoom, Messages
from .forms import MessagesForm
# Create your views here.

@login_required
def chat_view(request):
    chat_room = get_object_or_404(ChatRoom, chat_name = 'chat1')
    chat_messages = chat_room.chat_messages.all()
    
    form = MessagesForm()
    
    if request.method == 'POST':
        print(request)
        form = MessagesForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.chat = chat_room
            message.save()
            
            context = {
                'message' : message,
                'user' : request.user
            }
            
            print('message create')
            return render(request, 'core/chat_message_a.html', context)
        else:
            form = MessagesForm()
            
    return render(request, 'core/chats.html', {'chat_messages' : chat_messages, 'chat_room' : chat_room, 'form' : form})



@login_required
def chatSearch(request):
    from django.http import JsonResponse
    from django.template.loader import render_to_string
    from user.models import User

    if request.method == 'POST':
        print('post')
        search_data = request.POST.get('search')
        if search_data:
            if '@' in search_data:
                chats = User.objects.filter(email__contains=search_data).all()
            else:
                chats = User.objects.filter(username__contains=search_data).all()
            html = render_to_string('core/chatSearch.html', {'chats': chats})

            return JsonResponse({'status': 'success', 'html': html})
    
    return JsonResponse({'status': 'failed', 'error': 'invalid request'}), 400
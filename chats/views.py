from asgiref.sync import async_to_sync
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404
from .models import ChatRoom, Messages
from channels.layers import get_channel_layer
from .forms import MessagesForm
# Create your views here.

@login_required
def chat_view(request, chatroom_name='public-chat'):
    chat_group = get_object_or_404(ChatRoom, group_name=chatroom_name)
    chat_messages = chat_group.chat_messages.all()
    form = MessagesForm()
    
    other_user = None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404()
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                break
    
    if request.htmx:
        form = MessagesForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.chat = chat_group
            message.save()
            
            context = {
                'message' : message,
                'user' : request.user
            }
            
            return render(request, 'core/chat_message_a.html', context)
        else:
            form = MessagesForm()
            
    return render(request, 'core/chats.html', {'chat_messages' : chat_messages, 'chat_group' : chat_group, 'form' : form, 'other_user' : other_user, 'chatroom_name' : chatroom_name})

@login_required
def chat_redirect(request):
    return redirect('chat')

@login_required
def chatSearch(request):
    from django.http import JsonResponse
    from django.template.loader import render_to_string
    from user.models import User

    if request.method == 'POST':
        search_data = request.POST.get('search')
        if search_data:
            if '@' in search_data:
                chats = User.objects.filter(email__contains=search_data).all()
            else:
                chats = User.objects.filter(username__contains=search_data).all()
            html = render_to_string('core/chatSearch.html', {'chats': chats, 'user': request.user})

            return JsonResponse({'status': 'success', 'html': html})
    
    return JsonResponse({'status': 'failed', 'error': 'invalid request'}), 400


@login_required
def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect('chats')
    
    other_user = User.objects.get(username = username)
    my_chatrooms = request.user.chat_groups.filter(is_private=True)
    
    ot_us=''
    
    for chat in my_chatrooms:
        if chat.members.filter(id=other_user.id).exists():
            ot_us='1'
            break
        else:
            ot_us='2'    
    
    
    
    if my_chatrooms.exists():
        for chatroom in my_chatrooms:
            if other_user in chatroom.members.all():
                chatroom = chatroom
                break
            else:
                if ot_us=='2':
                    chatroom = ChatRoom.objects.create(is_private = True)
                    chatroom.members.add(other_user, request.user)
                    ot_us=''
    else:
        chatroom = ChatRoom.objects.create(is_private = True)
        chatroom.members.add(other_user, request.user)
        
        
    return redirect('chatroom', chatroom_name=chatroom.group_name)

@login_required
def chat_file_upload(request, chatroom_name):
    chat_group = get_object_or_404(ChatRoom, group_name=chatroom_name)

    if request.htmx and request.FILES:
        file = request.FILES['file']
        message = Messages.objects.create(author=request.user, chat=chat_group, file=file)
        
        chanel_layer = get_channel_layer()
        event = {
            'type': 'message_handler',
            'message_id': message.id,
        }
        async_to_sync(chanel_layer.group_send)(chatroom_name, event)
    return HttpResponse()
                
    
from channels.generic.websocket import WebsocketConsumer
import json
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
from .models import ChatRoom, Messages

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(ChatRoom, chat_name=self.chatroom_name)
        
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name, self.channel_name
        )
        self.accept()
        
        
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name, self.channel_name
        )
        
    
        
    def receive(self, text_data):
        text_data_json = json.loads(text_data) 
        content = text_data_json['content']
        
        message = Messages.objects.create(chat=self.chatroom, author=self.user, content=content)
        
        
        event = {
            'type' : 'message_handler',
            'message_id' : message.id
        }
        
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )
        
    def message_handler(self, event):
        message_id = event['message_id'] 
        message = Messages.objects.get(id=message_id)
        context = {
            'message' : message,
            'user' : self.user
        }
        
        html = render_to_string("core/chat_message_a.html", context=context)
        self.send(text_data=html)
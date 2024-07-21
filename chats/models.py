from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ChatRoom(models.Model):
    chat_name = models.CharField(max_length=244, unique=True)
    
    def __ste__(self):
        return self.group_chat
    
class Messages(models.Model):
    chat = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='chat_messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=280)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.author.username} : {self.content}"
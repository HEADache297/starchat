from django.db import models
from django.contrib.auth.models import User
import shortuuid

# Create your models here.

class ChatRoom(models.Model):
    group_name = models.CharField(max_length=128, unique=True, blank=True, default=shortuuid.uuid)
    users_online = models.ManyToManyField(User, related_name='online_in_groups', blank=True)
    members = models.ManyToManyField(User, related_name='chat_groups', blank=True)
    is_private = models.BooleanField(default=False)
        
    def __str__(self):
        return self.group_name
    
class Messages(models.Model):
    chat = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='chat_messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=280)
    created = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='files/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.author.username} : {self.content}"
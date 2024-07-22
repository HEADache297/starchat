from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('chats/', views.chat_view, name='chats'),
    path('chat/search/', views.chatSearch, name='chatSearch'),
    path('chat/<username>', views.get_or_create_chatroom, name="start-chat"),
    path('chat/room/<chatroom_name>', views.chat_view, name="chatroom"),
]
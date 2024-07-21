from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('chats/', views.chat_view, name='chats'),
    path('chat/search/', views.chatSearch, name='chatSearch'),
]
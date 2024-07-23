from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('chats/', views.chat_view, name='chats'),
    path('chat/search/', views.chatSearch, name='chatSearch'),
    path('chat/<username>', views.get_or_create_chatroom, name="start-chat"),
    path('chat/room/<chatroom_name>', views.chat_view, name="chatroom"),
    path('chat/fileupload/<chatroom_name>', views.chat_file_upload, name='chat-file-upload')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.shortcuts import render

# Create your views here.

def chats(request):
    return render(request, 'core/chats.html')
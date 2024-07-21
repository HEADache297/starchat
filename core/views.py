from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def chats(request):
    return render(request, 'core/chats.html')

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
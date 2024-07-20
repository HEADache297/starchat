from django.shortcuts import render, redirect,HttpResponse
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.shortcuts import get_object_or_404
from .models import Profile
from django.contrib.auth.decorators import login_required
from .forms import ChangeImageForm

# Create your views here.

def home(request):
    return HttpResponse('Home page')
    
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            
            profile = Profile(user=user)
            profile.save()
            print(form.cleaned_data.get('email'))
            print('form save')
            return redirect('login')
    else:
        form = SignUpForm()
        
    return render(request, 'auth/signup.html', {'form' : form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)   
        if form.is_valid:
            print(form)
            print(form.cleaned_data.get('username'))                               
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(username = username,
                                password = password)



            if user is not None:
                auth_login(request, user)
                print(user)
                return redirect('chats')
    else: 
        form = LoginForm()
    return render(request, 'auth/login.html', {'form' : form})

def logout(request):
    from django.contrib.auth import logout
    logout(request)

    return redirect('login')


def profile(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    form=ChangeImageForm()
    if request.method == "POST":
        form = ChangeImageForm(request.POST, request.FILES)
        if form.is_valid():
            profile.image = form.cleaned_data.get('image')
            profile.save()
    return render(request, 'profile/profile.html', {'profile':profile,'form':form})
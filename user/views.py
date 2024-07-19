from django.shortcuts import render, redirect,HttpResponse
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

# Create your views here.

def home(request):
    return HttpResponse('Home page')
    
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            print(form.cleaned_data.get('email'))
            print('form save')
            return redirect('hhome')
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
                return redirect('hhome')
    else: 
        form = LoginForm()
    return render(request, 'auth/login.html', {'form' : form})

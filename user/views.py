from django.shortcuts import render, redirect,HttpResponse
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.shortcuts import get_object_or_404
from .models import Profile
from django.contrib.auth.decorators import login_required
from .forms import ChangeImageForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

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
            email = create_email(
                request,
                user,
                'Activate your user account!',
                'users/activation.html')

            if email.send():
                messages.success(request, 'Check your email and confirm your account!')
                return redirect('login')
            else:
                messages.error(request, 'Something went wrong with your email. Try it later...')
                return redirect('signup')
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
                #if user.is_authenticated==True:
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


def create_email(request, user, subject: str, html_page: str):
    from .token import account_activation_token
    from django.contrib.sites.shortcuts import get_current_site
    message = render_to_string(html_page, {'user': user,
                                           'domain': get_current_site(request).domain,
                                           'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                           'token': account_activation_token.make_token(user),
                                           'protocol': 'https' if request.is_secure() else 'http'}
                               )

    text_message = strip_tags(message)

    email = EmailMultiAlternatives(subject, text_message, to=[user.email])
    email.attach_alternative(message, 'text/html')
    return email

def activate_user(request, uid, token):
    from .token import account_activation_token
    print('User id:', uid, 'secret token', token)
    try:
        from django.contrib.auth.models import User
        uid = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated successfully!")
        redirect('/login')
    else:
        messages.success(request, "Invalid activation link")
    return redirect('login')
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/<slug:slug>', views.profile, name='profile'),
    path('activate/<uid>/<token>', views.activate_user, name='activate_user'),
    path('profile/password/change', views.change_password, name='change_user_password'),
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
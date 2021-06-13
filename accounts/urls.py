# accounts/urls.py
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views as core_views

from .views import SignUpView

urlpatterns = [
    path('', core_views.home, name='home'),
    path('signup/', core_views.signup, name='signup'),
    path('profile/', core_views.profile, name='profile'),
    #path('profile/', core_views.ProfileView.as_view(), name='profile'),
    path('account_activation_sent/', core_views.account_activation_sent, name='account_activation_sent'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,50})/$',
         core_views.activate, name='activate'),
    #path('signup/', SignUpView.as_view(), name='signup'),
]
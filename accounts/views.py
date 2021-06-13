# accounts/views.py
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse

from django.views import generic
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from .forms import SignUpForm, ProfileUpdateForm, UserUpdateForm
from .models import Profile
from .tokens import account_activation_token


@login_required
def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user_group = Group.objects.get(name='visitors')
            user.groups.add(user_group)

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class ProfileView(LoginRequiredMixin, generic.UpdateView):
    model = Profile
    login_url = '/accounts/login/'
    template_name = 'registration/profile.html'
    fields = ['bio', 'avatar', 'location', 'birth_date']
    success_url = reverse_lazy('profile')

    # PK required in UpdateView, making context['object']
    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            queryset = Profile.objects.get(user=self.request.user)
        return queryset


@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        u_form = UserUpdateForm(request.POST,instance=request.user)
        if p_form.is_valid() and u_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,'Your Profile has been updated!')
            return redirect('profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
        u_form = UserUpdateForm(instance=request.user)

    context={'p_form': p_form, 'u_form': u_form}
    return render(request, 'profile.html', context )
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    first_name = forms.CharField(max_length=50, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=50, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username', 'first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'location', 'birth_date',]

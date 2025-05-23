from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.models import User

class ProfileCreationForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ('username', 'email', 'address', 'C')

class UserRegisterForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=Profile.USER_TYPE)
    phone = forms.CharField()
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','address', 'phone']

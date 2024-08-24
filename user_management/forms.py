from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import CustomUser

class RegisterUserForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'type': 'password', 'name': 'password1', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'type': 'password', 'name': 'password2', 'placeholder': 'Repeat you password'}))

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input', 'type': 'text', 'name': 'first_name', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'input', 'type': 'text', 'name': 'last_name', 'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'class': 'input', 'type': 'email', 'name': 'email', 'placeholder': 'Email'}),
            'username': forms.TextInput(attrs={'class': 'input', 'type': 'text', 'name': 'username', 'placeholder': 'Username'}),
            'password1': forms.PasswordInput(attrs={'class': 'input', 'type': 'password', 'name': 'password1', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'input', 'type': 'password', 'name': 'password2', 'placeholder': 'Repeat you password'}),
        }

class LoginUserForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input', 'type': 'email', 'name': 'email', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'type': 'password', 'name': 'password', 'placeholder': 'Password'}))

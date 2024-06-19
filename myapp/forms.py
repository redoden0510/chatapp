from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Message
from allauth.account.forms import LoginForm as AllAuthLoginForm 

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'icon']
        
class CustomLoginForm(AllAuthLoginForm):
    username = forms.CharField(max_length=150, required=True, label='ユーザーネーム')
    email = forms.EmailField(required=True, label='メールアドレス')
    password = forms.CharField(widget=forms.PasswordInput, label='パスワード')

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "password"]

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
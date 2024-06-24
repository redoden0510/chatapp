from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Message
from allauth.account.forms import LoginForm as AllAuthLoginForm, SignupForm


class CustomUserCreationForm(SignupForm):
    user_name = forms.CharField(max_length=30, label="ユーザーネーム")
    icon = forms.ImageField(allow_empty_file=True, required=False)
    
    class Meta:
        model = CustomUser
        fields = ['user_name', 'email', 'password1', 'password2', 'icon']
        
    def signup(self, request, user):
        user.username = self.cleaned_data["user_name"]
        user.icon= self.cleaned_data["icon"]
        user.save()
        return user
        
class CustomLoginForm(AllAuthLoginForm):
    password = forms.CharField(widget=forms.PasswordInput, label='パスワード')

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
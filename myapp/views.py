from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from .forms import CustomUserCreationForm, LoginForm, MessageForm
from django.views.generic import CreateView, ListView, TemplateView
from .models import CustomUser, Message, User
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.views.generic.edit import UpdateView
from django.db.models import Q


def index(request):
    return render(request, "myapp/index.html")

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    model= CustomUser
    success_url = reverse_lazy('index')  # ユーザーが登録後にリダイレクトされるURL
    template_name = 'myapp/signup.html'  # ユーザー登録フォームを含むテンプレート

# class Login(LoginView):
#     form = LoginForm
#     template_name = "myapp/login.html"
#     success_url = 'friends'
    
#     def form_valid(self, form):
#         # ログインフォームのデータを取得
#         username = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password')

#         # ユーザーを認証
#         user = authenticate(username=username, password=password)

#         if user is not None:
#             # ユーザーが存在する場合、ログインする
#             login(self.request, user)

#             # UserProfileが存在しない場合、作成する
#             # if not CustomUser.objects.filter(user=user).exists():
#             #     CustomUser.objects.create(user=user)

#         return redirect(self.success_url)

class Friend(LoginRequiredMixin, ListView):
    template_name = 'myapp/friends.html'
    context_object_name = 'users'
    model = CustomUser
    
    # def get_queryset(self):
    #     user=CustomUser.objects.exclude(id=self.request.user.id)
    #     return user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # friend_id = self.kwargs['id']  # URLのパラメータからfriend_idを取得
        # friend = get_object_or_404(CustomUser, id=friend_id)  # CustomUserインスタンスを取得
        friends=CustomUser.objects.exclude(id=self.request.user.id)
        context['users'] = friends
        
        # print(Message.objects.filter(sender=CustomUser.objects.exclude(id=self.request.user.id)))
 
        latest_chat = Message.objects.filter(
            Q(sender=self.request.user) | 
            Q(recipient=self.request.user)
            ).order_by('-timestamp').last
        context['latest_chat'] = latest_chat
        print(latest_chat)
        
        # latest_chat = latest_chat = Message.objects.filter(
        #     Q(sender=self.request.user) & Q(recipient=friends) | 
        #     Q(sender=friends) & Q(recipient=self.request.user)
        #     ).order_by('-timestamp').last
        # context['latest_chat'] = latest_chat
        # context['friend'] = friend
        
        
        # latest_chat = Message.objects.filter(
        #     Q(sender=self.request.user) & Q(recipient=friend) | 
        #     Q(sender=friend) & Q(recipient=self.request.user)
        #     ).order_by('-timestamp').last
        # context['latest_chat'] = latest_chat
        return context

class Talk(FormView):
    form_class = MessageForm
    template_name = 'myapp/talk_room.html'
    model = CustomUser

    def get_success_url(self) -> str:
        return reverse("talk_room",kwargs={"pk":self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        friend_id = self.kwargs['pk']  # URLのパラメータからfriend_idを取得
        friend = get_object_or_404(CustomUser, id=friend_id)  # CustomUserインスタンスを取得
        context['friend'] = friend
        messages = Message.objects.filter(
            Q(sender=self.request.user) & Q(recipient=friend) | 
            Q(sender=friend) & Q(recipient=self.request.user)
            ).order_by('-timestamp')[:10]
        context['messages'] = messages
        return context
    
    def form_valid(self, form):
        friend_id = self.kwargs['pk']
        friend = get_object_or_404(CustomUser, id=friend_id)
        sender = self.request.user
        recipient = friend
        content=form.cleaned_data['content']

        # メッセージを作成して保存
        Message.objects.create(
        sender=sender,
        recipient=recipient,
        content=content
        )
        return redirect(self.get_success_url())

def setting(request):
    context = {
        'pk': request.user.pk,
    }
    return render(request, "myapp/setting.html", context)

class c_un(UpdateView):
    model = CustomUser
    fields = ['username']
    template_name = 'myapp/c_un.html'
    success_url = reverse_lazy('setting')

class c_ma(UpdateView):
    model = CustomUser
    fields = ['email']
    template_name = 'myapp/c_ma.html'
    success_url = reverse_lazy('setting')

class c_ic(UpdateView):
    model = CustomUser
    fields = ['icon']
    template_name = 'myapp/c_ic.html'
    success_url = reverse_lazy('setting')
    
class c_pw(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('setting')
    template_name = 'myapp/c_pw.html'

class logout(LogoutView):
    template_name = 'myapp/logout.html'
    next_page = 'logout'
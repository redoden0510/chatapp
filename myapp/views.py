from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from .forms import CustomUserCreationForm, LoginForm, MessageForm
from django.views.generic import CreateView, ListView, TemplateView
from .models import CustomUser, Friends, Message, User
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.views.generic.edit import UpdateView


def index(request):
    return render(request, "myapp/index.html")

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    model= CustomUser
    success_url = reverse_lazy('index')  # ユーザーが登録後にリダイレクトされるURL
    template_name = 'myapp/signup.html'  # ユーザー登録フォームを含むテンプレート

class Login(LoginView):
    form = LoginForm
    template_name = "myapp/login.html"
    success_url = 'friends'
    
    def form_valid(self, form):
        # ログインフォームのデータを取得
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        # ユーザーを認証
        user = authenticate(username=username, password=password)

        if user is not None:
            # ユーザーが存在する場合、ログインする
            login(self.request, user)

            # UserProfileが存在しない場合、作成する
            if not Friends.objects.filter(user=user).exists():
                Friends.objects.create(user=user)

        return redirect(self.success_url)

class Friend(LoginRequiredMixin, ListView):
    model = Friends
    template_name = 'myapp/friends.html'
    context_object_name = 'friends'
    # paginate_by = 4
    # friend=CustomUser.objects.exclude(id=self.request.user.id)
    # friend_ids = [user.id for user in friend]
    
    def get_queryset(self):
        friend=Friends.objects.exclude(id=self.request.user.id)
        return friend
    
    def get_friend_ids(self, friend):
        friend_ids = [user.id for user in friend]
        print(friend_ids)
        return friend_ids
    
    
class Talk(ListView):
    form_class = MessageForm
    template_name = 'myapp/talk_room.html'
    model = Message, Friends
    success_url = reverse_lazy('talk_room/<int:friend_id>/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # friend_id = self.friend.id
        # トークルームの友人を取得
        friend = get_object_or_404(Friends, pk=self.kwargs['user_id'])
        context['friend'] = friend
        
        messages = Message.objects.filter(sender=self.request.user, recipient=self.friend.user).order_by('-timestamp')[:10]
        context['messages'] = messages
        return context
    
    
    def form_valid(self, form):
        friend_id = self.friend.user.id
        # 受信者を取得するために、ログインしているユーザーの友人の中から選択されたユーザーを取得
        self.friend = get_object_or_404(Friends,pk=self.kwargs['friend_id'], user=self.request.user)
         # メッセージの送信者はログインしているユーザー
        sender = self.request.user
        recipient = self.friend.user

        # メッセージを作成して保存
        Message.objects.create(
        sender=sender,
        recipient=recipient,
        content=form.cleaned_data['content']
        )

        return HttpResponseRedirect(reverse('talk_room/<int:friend_id>/'), args=[friend_id]), sender
        
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
# from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from .forms import CustomUserCreationForm, CustomLoginForm, MessageForm
from django.views.generic import CreateView, ListView, TemplateView
from .models import CustomUser, Message, User
from django.contrib.auth.views import PasswordChangeView, LogoutView
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
# from django.http import HttpResponseRedirect
from django.views.generic.edit import UpdateView
from django.db.models import Q
from django.core.paginator import Paginator



def index(request):
    return render(request, "myapp/index.html")


class Friend(LoginRequiredMixin, ListView):
    template_name = 'myapp/friends.html'
    context_object_name = 'users'
    model = CustomUser
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        friends = CustomUser.objects.exclude(id=self.request.user.id)
        query = self.request.GET.get('query', '')

        if query:
            friends = friends.filter(
                Q(username__icontains=query) |
                Q(email__icontains=query))

        friend_ids = friends.values_list('id', flat=True)

        # 友達とユーザー間の最新メッセージを取得
        latest_messages = Message.objects.filter(
            Q(sender__in=friend_ids, recipient=self.request.user) |
            Q(sender=self.request.user, recipient__in=friend_ids)
        ).select_related('sender', 'recipient').order_by('sender', 'recipient', '-timestamp').distinct('sender', 'recipient')

        latest_messages_dict = {}
        for message in latest_messages:
            if message.sender_id == self.request.user.id:
                latest_messages_dict[message.recipient_id] = message
            else:
                latest_messages_dict[message.sender_id] = message

        latest_chats = []
        no_chat_friends = []

        for friend in friends:
            latest_chat = latest_messages_dict.get(friend.id, None)
            if latest_chat:
                latest_chats.append((friend, latest_chat))
            else:
                no_chat_friends.append(friend)

        # 最新メッセージの送信日時でソート（降順）
        latest_chats.sort(key=lambda x: x[1].timestamp if x[1] else None, reverse=True)

        for friend in no_chat_friends:
            latest_chats.append((friend, None))

        paginator = Paginator(latest_chats, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['latest_chats'] = page_obj.object_list
        context['is_paginated'] = page_obj.has_other_pages()
        context['page_obj'] = page_obj
        context['query'] = query

        if not latest_chats:
            context['no_friends_message'] = "該当するフレンドが存在しません"

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
            ).order_by('timestamp')
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
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.SignUp.as_view(), name='signup'),
    path('login', views.Login.as_view(), name='login'),
    path('friends', views.Friend.as_view(), name='friends'),
    path('talk_room/<int:pk>', views.Talk.as_view(), name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('username_change/<int:pk>', views.c_un.as_view(), name='c_un'),
    path('mail_change/<int:pk>', views.c_ma.as_view(), name='c_ma'),
    path('icon_change/<int:pk>', views.c_ic.as_view(), name='c_ic'),
    path('password_change/<int:pk>', views.c_pw.as_view(), name='c_pw'),
    path('logout', views.logout.as_view(), name='logout'),
]

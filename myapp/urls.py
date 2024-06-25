from django.urls import path
from . import views
# from django.conf import settings
# from django.conf.urls.static import static
# from django.contrib.auth.views import LoginView
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.index, name='index'),
    path('friends', views.Friend.as_view(), name='friends'),
    path('talk_room/<int:pk>', views.Talk.as_view(), name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('username_change/<int:pk>', views.c_un.as_view(), name='c_un'),
    path('mail_change/<int:pk>', views.c_ma.as_view(), name='c_ma'),
    path('icon_change/<int:pk>', views.c_ic.as_view(), name='c_ic'),
    path('password_change/<int:pk>', views.c_pw.as_view(), name='c_pw'),
    path('logout', views.logout.as_view(), name='logout'),
] 

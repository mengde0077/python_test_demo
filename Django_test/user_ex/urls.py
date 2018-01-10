#coding:utf-8
from django.conf.urls import include, url
from user_ex import views

#start with 'user/'
urlpatterns = [
    url(r'^me$', views.me, name='me'),
    url(r'^check_is_login$',views.check_is_login,name='check_is_login'),
    url(r'^user_logout$',views.user_logout,name='user_logout'),
    url(r'^user_login$',views.user_login,name='user_login'),
    url(r'^user_reg$',views.user_reg,name='user_reg'),
    url(r'^user_active/([a-zA-Z]+)$','user_ex.views.user_active',name='user_active'),
]

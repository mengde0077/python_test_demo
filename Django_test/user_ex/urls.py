#coding:utf-8
from django.conf.urls import include, url
from user_ex import views

#start with 'user/'
urlpatterns = [
    url(r'^login_page$','user_ex.views.login_page',name='login_page'),
    url(r'^user_info$','user_ex.views.user_info',name='user_info'),
    url(r'^check_is_login$',views.check_is_login,name='check_is_login'),
    url(r'^user_logout$',views.user_logout,name='user_logout'),
    url(r'^user_login$',views.user_login,name='user_login'),
    url(r'^user_reg$',views.user_reg,name='user_reg'),
    url(r'^user_active/([a-zA-Z]+)$',views.user_active,name='user_active'),
    url(r'^nickname_change$',views.nickname_change,name='nickname_change'),
    url(r'^password_change$','user_ex.views.password_change',name='password_change'),
    url(r'^password_lost$', 'user_ex.views.password_lost', name='password_lost'),
    url(r'^get_email_code$', 'user_ex.views.get_email_code', name='get_email_code'),

]

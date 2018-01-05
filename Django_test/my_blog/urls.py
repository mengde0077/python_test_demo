#coding:utf-8
"""Django_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from . import views as my_blog_views
from django.conf import settings



urlpatterns = [
    url(r'^bloglist/$', my_blog_views.blog_list, name='bloglist'),
    # name属性是给这个url起个别名，可以在模版中引用而不用担心urls文件中url的修改 引用方式为{% url blog_list %}
    url(r'^blog/(?P<id>\d+)/$', my_blog_views.blog_show, name='detailblog'),
    url(r'^blog/tag/(?P<id>\d+)/$', my_blog_views.blog_filter, name='filtrblog'),
    url(r'^blog/search/$', my_blog_views.blog_search, name='searchblog'),
    url(r'^blog/add/$', my_blog_views.blog_add, name='addblog'),
    url(r'^blog/(?P<id>\w+)/update/$', my_blog_views.blog_update, name='updateblog'),
    url(r'^blog/(?P<id>\w+)/del/$', my_blog_views.blog_del, name='delblog'),
    url(r'^blog/addmassage/$', my_blog_views.add_weibo, name='addmassage'),
    url(r'^blog/showweibo/$', my_blog_views.show_weibo, name='showweibo'),
    url(r'^blog/(?P<id>\d+)/commentshow/$', my_blog_views.blog_show_comment, name='showcomment'),


]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

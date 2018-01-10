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
from django.contrib import admin
from DjangoUeditor import urls as DjangoUeditor_url
from test_app import views as test_app_views
import views
from django.conf import settings
from user_ex import urls as user_ex_urls
from my_blog import urls as blog_urls
from django_comments import urls as django_comments_urls

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about$', views.about, name='about'),
    url(r'^contact$', views.contact, name='contact'),
    url(r'^single$', views.single, name='single'),
    url(r'^baidutongji$', views.baidutongji, name='baidutongji'),
    url(r'^news$', test_app_views.news, name='news'),
    #注意include()函数的正则表达式的末尾没有$
    url(r'^sblog/', include(blog_urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ueditor/', include(DjangoUeditor_url)),
    url(r'^user/',include(user_ex_urls)),    #加载 user_ex包下的urls文件配置
    url(r'^comments/', include(django_comments_urls)),
    url(r'^column/(?P<column_slug>[^/]+)/$', test_app_views.column_detail, name='column'),
    url(r'^article/(?P<pk>\d+)/(?P<article_slug>[^/]+)/$', test_app_views.article_detail, name='article'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#coding: utf-8
from django.template import RequestContext
from django.shortcuts import render
from django.http import HttpRequest
from my_blog.models import Blog,Tag,Author,Weibo
from helper.paginator import getPages  #导入helper文件夹的分页通用方法


def index(request):
    # 倒序获取
    blogs = Blog.objects.order_by('-read_num')
    pages, blogs = getPages(request, blogs) #分页处理
    tags = Tag.objects.all()
    #获取最新的 5条 评论
    weibos = Weibo.objects.order_by('-publish_time')[:5]
    return render(request, "index.html",
        {"blogs": blogs, "pages":pages, "tags": tags, "weibos": weibos},
        context_instance=RequestContext(request))


def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def single(request):
    return render(request, 'single.html')

def baidutongji(request):
    return render(request, 'baidutongji.html')

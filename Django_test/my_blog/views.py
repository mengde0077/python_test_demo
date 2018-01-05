#coding:utf-8
from django.template import RequestContext
from django.shortcuts import render
from helper.paginator import getPages  #导入helper文件夹的分页通用方法
from models import Blog,Tag,Author,Weibo
from forms import BlogForm,TagForm
from django.core.paginator import Paginator
from django.http import Http404,HttpResponseRedirect

def blog_list(request):
    # 倒序获取
    blogs = Blog.objects.order_by('-id')
    pages, blogs = getPages(request, blogs) #分页处理
    tags = Tag.objects.all()
    #获取最新的 5条 评论
    weibos = Weibo.objects.order_by('-publish_time')[:5]
    return render(request, "blog/blog_list.html",
        {"blogs": blogs, "pages":pages, "tags": tags, "weibos": weibos},
        context_instance=RequestContext(request))


def blog_show(request, id=''):
    try:
        blog = Blog.objects.get(id=id)
        blog.read_num += 1
        blog.save()
    except Blog.DoesNotExist:
        raise Http404("没有这个帖子")
    return render(request, 'blog/blog_show.html' ,{"blog": blog})

def blog_filter(request, id=''):
    tags = Tag.objects.all()
    tag =  Tag.objects.get(id=id)
    blogs = tag.blog_set.all()
    return render(request, "blog/blog_filter.html",
        {"blogs": blogs, "tag": tag, "tags": tags})

def blog_show_comment(request, id=''):
    blog = Blog.objects.get(id=id)
    return render(request, 'blog/blog_comments_show.html', {"blog": blog})


def blog_search(request):
    tags = Tag.objects.all()
    if 'search' in request.GET:
        search = request.GET['search']
        blogs = Blog.objects.filter(caption__icontains=search)
        return render(request, 'blog/blog_filter.html',
            {"blogs": blogs, "tags": tags}, context_instance=RequestContext(request))
    else:
        blogs = Blog.objects.order_by('-id')
        return render(request, "blog/blog_list.html", {"blogs": blogs, "tags": tags},
            context_instance=RequestContext(request))


def blog_add(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        tag = TagForm(request.POST)
        if form.is_valid() and tag.is_valid():
            cd = form.cleaned_data
            cdtag = tag.cleaned_data
            tagname = cdtag['tag_name']
            for taglist in tagname.split():
                Tag.objects.get_or_create(tag_name=taglist.strip())
            title = cd['caption']
            author = Author.objects.get(id=1)
            content = cd['content']
            blog = Blog(caption=title, author=author, content=content)
            blog.save()
            for taglist in tagname.split():
                blog.tags.add(Tag.objects.get(tag_name=taglist.strip()))
                blog.save()
            id = Blog.objects.order_by('-publish_time')[0].id
            return HttpResponseRedirect('/sblog/blog/%s' % id)
    else:
        form = BlogForm()
        tag = TagForm()
    return render(request, 'blog/blog_add.html',
        {'form': form, 'tag': tag}, context_instance=RequestContext(request))

def show_weibo(request):
    weibos = Weibo.objects.order_by('-publish_time')[:5]
    return render("blog/blog_twitter.html", {"weibos": weibos})


def add_weibo(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        massage = request.POST['twitter']
        author = Author.objects.get(id=1)
        massage = Weibo(massage=massage, author=author)
        massage.save()
        weibos = Weibo.objects.order_by('-publish_time')[:5]
        return render(request, "blog/blog_twitter.html",
        {"weibos": weibos},
        context_instance=RequestContext(request))
    else:
        return HttpResponse('dddd')



def blog_update(request, id=""):
    id = id
    if request.method == 'POST':
        form = BlogForm(request.POST)
        tag = TagForm(request.POST)
        if form.is_valid() and tag.is_valid():
            cd = form.cleaned_data
            cdtag = tag.cleaned_data
            tagname = cdtag['tag_name']
            tagnamelist = tagname.split()
            for taglist in tagnamelist:
                Tag.objects.get_or_create(tag_name=taglist.strip())
            title = cd['caption']
            content = cd['content']
            blog = Blog.objects.get(id=id)
            if blog:
                blog.caption = title
                blog.content = content
                blog.save()
                for taglist in tagnamelist:
                    blog.tags.add(Tag.objects.get(tag_name=taglist.strip()))
                    blog.save()
                tags = blog.tags.all()
                for tagname in tags:
                    tagname = unicode(str(tagname), "utf-8")
                    if tagname not in tagnamelist:
                        notag = blog.tags.get(tag_name=tagname)
                        blog.tags.remove(notag)
            else:
                blog = Blog(caption=blog.caption, content=blog.content)
                blog.save()
            return HttpResponseRedirect('/sblog/blog/%s' % id)
    else:
        try:
            blog = Blog.objects.get(id=id)
        except Exception:
            raise Http404
        form = BlogForm(initial={'caption': blog.caption, 'content': blog.content}, auto_id=False)
        tags = blog.tags.all()
        if tags:
            taginit = ''
            for x in tags:
                taginit += str(x) + ' '
            tag = TagForm(initial={'tag_name': taginit})
        else:
            tag = TagForm()
    return render(request, 'blog/blog_add.html',
        {'blog': blog, 'form': form, 'id': id, 'tag': tag},
        context_instance=RequestContext(request))

def blog_del(request, id=""):
    try:
        blog = Blog.objects.get(id=id)
    except Exception:
        raise Http404("删除对象不存在")
    if blog:
        blog.delete()
        return HttpResponseRedirect("/sblog/")
    blogs = Blog.objects.all()
    return render(request, "blog/blog_list.html", {"blogs": blogs})




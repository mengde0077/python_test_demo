#coding: utf-8
from django.core.paginator import Paginator  #导入分页器
from django.shortcuts import render
from .models import Column, Article
from django.http import HttpRequest

def news(request):
    columns =Column.objects.all()
    home_display_columns = Column.objects.filter(home_display=True)
    nav_display_columns = Column.objects.filter(nav_display=True)

    return render(request, 'news.html', {
        'columns': columns,
        'home_display_columns': home_display_columns,
        'nav_display_columns': nav_display_columns,
        })


def column_detail(request, column_slug):
    column = Column.objects.get(slug=column_slug)
    return render(request, 'test_app/column.html' , {'column': column})

def article_detail(request, pk, article_slug):
    # 一次能获取3条数据
    # article = Article.objects.get(slug=artile_slug)
    #带上 pk 主键
    article =Article.objects.get(pk=pk)

    if article_slug != article_slug:
        return redirect(article, permanent=True)

    return render(request, 'test_app/article.html' , {'article': article})

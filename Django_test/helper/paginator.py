# -*- coding: utf-8 -*-
from django.core.paginator import Paginator
from django.conf import settings

def getPages(request, objectlist):
    """get the paginator"""
    #获取GET请求的参数，得到当前页码。若没有该参数，默认为1
    currentPage = request.GET.get('page', 1)
    #2个对象为1页，这个参数可以写在settings.py里面
    paginator = Paginator(objectlist, settings.EACHPAGE_NUMBER)
    objectlist = paginator.page(currentPage)

    return paginator, objectlist

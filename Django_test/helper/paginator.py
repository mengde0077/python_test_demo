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

    page_range = []
    current = objectlist.number     #当前页码
    page_all = paginator.num_pages  #总页数
    mid_pages = 3                   #中间段显示的页码数
    page_goto = 1                   #默认跳转的页码

    #获取优化显示的页码列表
    if page_all <= 2 + mid_pages:
        #页码数少于6页就无需分析哪些地方需要隐藏
        page_range = paginator.page_range
        print "page_range1: ", page_range
    else:
        #添加应该显示的页码
        page_range += [1, page_all]
        print "page_range2: ", page_range
        page_range += [current-1, current, current-2]
        print "page_range3: ", page_range

        #若当前页是头尾，范围拓展多1页
        if current == 1 or current == page_all:
            page_range += [current+2, current-2]
            print "page_range4: ", page_range

        #去掉超出范围的页码
        page_range = filter(lambda x: x>=1 and x<=page_all, page_range)
        print "page_range5: ", page_range

        #排序去重
        page_range = sorted(list(set(page_range)))
        print "page_range6: ", page_range

        #查漏补缺
        #从第2个开始遍历，查看页码间隔，若间隔为0则是连续的
        #若间隔为1则补上页码；间隔超过1，则补上省略号
        t = 1
        for i in range(len(page_range)-1):
            step = page_range[t]-page_range[t-1]
            if step>=2:
                if step==2:
                    page_range.insert(t,page_range[t]-1)
                    print "page_range7: ", page_range
                else:
                    page_goto = page_range[t-1] + 1
                    page_range.insert(t,'...')
                    print "page_range8: ", page_range
                t+=1
            t+=1

    #优化结果之后的页码列表
    paginator.page_range_ex = page_range
    #默认跳转页的值
    paginator.page_goto = page_goto

    return paginator,objectlist




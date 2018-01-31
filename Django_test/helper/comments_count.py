# -*- coding: utf-8 -*-
#coding:utf-8
from django.db import connection, transaction
import django_comments
from my_blog.models import Blog

def get_comments_count(user_id, content_type = 'my_blog'):
    """get the blog comments count"""
    #获得一个游标(cursor)对象
    cursor = connection.cursor()
    sql = ur"""
        select count(django_comments.id)
        from django_comments
        left join django_content_type
        on django_comments.content_type_id = django_content_type.id
        where django_content_type.app_label = %s and user_id = %s and root_id = 0
        """
    paras = [content_type, user_id]
    cursor.execute(sql, paras)    #执行sql语句
    raw = cursor.fetchone()       #获取第一行
    return raw[0]

def get_replies_count(user_id, content_type = 'my_blog'):
    """get the blog replies count"""
    #获得一个游标(cursor)对象
    cursor = connection.cursor()
    sql = ur"""
        select count(django_comments.id)
        from django_comments
        left join django_content_type
        on django_comments.content_type_id = django_content_type.id
        where django_content_type.app_label = %s and user_id = %s and root_id > 0
        """
    paras = [content_type, user_id]
    cursor.execute(sql, paras)    #执行sql语句
    raw = cursor.fetchone()       #获取第一行
    return raw[0]

def get_to_reply_count(user_id, content_type = 'my_blog'):
    """get to be replyed count"""
    #获得一个游标(cursor)对象
    cursor = connection.cursor()
    sql = ur"""
        select count(django_comments.id) from django_comments
        where user_id = %s and id in (
        select django_comments.reply_to
        from django_comments
        left join django_content_type
        on django_comments.content_type_id = django_content_type.id
        where django_content_type.app_label = %s and root_id>0)
        """
    paras = [user_id, content_type]
    cursor.execute(sql, paras)    #执行sql语句
    raw = cursor.fetchone()       #获取第一行
    return raw[0]

def last_talk_about(user_id, content_type = 'my_blog'):
    """get last talk about blog"""
    #获得一个游标(cursor)对象
    cursor = connection.cursor()
    sql = ur"""
        select django_comments.object_pk
        from django_comments
        left join django_content_type
        on django_comments.content_type_id = django_content_type.id
        where django_content_type.app_label = %s and user_id=%s
        order by submit_date desc limit 1
        """
    paras = [content_type, user_id]
    cursor.execute(sql, paras)    #执行sql语句
    raw = cursor.fetchone()       #获取第一行

    try:
        return Blog.objects.get(id = raw[0])
    except Exception as e:
        return None

def all_talk_about(user_id):
    """get all talk about blogs"""
    sql = ur"""
        select my_blog_blog.* from my_blog_blog
        where id in (select django_comments.object_pk
        from django_comments
        left join django_content_type
        on django_comments.content_type_id = django_content_type.id
        where django_content_type.app_label = 'my_blog' and user_id=%s)
        """ % user_id

    blogs=list(Blog.objects.raw(sql))   #raw_query对象是一个生成器
    comment_model = django_comments.get_model()

    for blog in blogs:
        sql = ur"""
                select django_comments.*
                from django_comments
                left join django_content_type
                on django_comments.content_type_id = django_content_type.id
                where django_content_type.app_label = 'my_blog' and user_id=%s and django_comments.object_pk='%s'
                order by submit_date desc
            """ % (user_id, blog.id)

        blog.comments = comment_model.objects.raw(sql)
    return blogs

#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: caolinming
# @Date:   2017-04-10 10:57:33
# @Last Modified by:   caolinming
# @Last Modified time: 2017-09-18 16:17:33
# 来源： https://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001386832360548a6491f20c62d427287739fcfa5d5be1f000
# ThreadLocal 的应用

import threading


def process_student(name):
	print 'Hello, %s (in %s)' % (name, threading.current_thread().name)

def process_thread(name):
	process_student(name)

t1 = threading.Thread(target=process_thread, args=('Alice',), name='Thread-A')
t2 = threading.Thread(target=process_thread, args=('Bob',), name='Thread-B')

t1.start()
t2.start()
t1.join()
t2.join()
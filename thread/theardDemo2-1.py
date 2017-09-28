#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: caolinming
# @Date:   2017-04-10 10:57:33
# @Last Modified by:   caolinming
# @Last Modified time: 2017-09-18 14:44:27
# 来源： https://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001386832360548a6491f20c62d427287739fcfa5d5be1f000


import threading
import time

# 新线程执行的代码：
def loop():
	print 'thread %s is running...' % threading.current_thread().name
	n = 0
	while n < 5:
		n = n + 1
		print 'thread %s >>> %s' % (threading.current_thread().name, n)
		time.sleep(1)
	print 'thread %s ended.' % threading.current_thread().name

print 'thread %s is running...' % threading.current_thread().name
t = threading.Thread(target=loop, name='LoopThread')
t.start()
t.join()

print 'thread %s ended.' % threading.current_thread().name
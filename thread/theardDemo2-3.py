#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: caolinming
# @Date:   2017-04-10 10:57:33
# @Last Modified by:   caolinming
# @Last Modified time: 2017-09-18 15:05:34
# 来源： https://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001386832360548a6491f20c62d427287739fcfa5d5be1f000


import threading
import time

# 假设 银行 存款 为 
balance = 0
# 加上一把锁  ，消耗时间会有所增加 ，相当于在 修改存款时，需要列队等待逐一执行
lock = threading.Lock()

def change_it(n):
	# 先存 后取， 结果应该为 0；
	global balance
	balance = balance + n
	balance = balance - n

def run_thread(n):
	for i in range(10000000):
		# 先要获取锁
		lock.acquire()
		try:
			# 放心的进行修改：
			change_it(n)
		finally:
			# 改完了一定要释放锁：
			lock.release()

print time.ctime(time.time())
t1 = threading.Thread(target=run_thread, args=(5,))
t2 = threading.Thread(target=run_thread, args=(8,))
t1.start()
t2.start()
t1.join()
t2.join()

print balance
print time.ctime(time.time())

# -*- coding: utf-8 -*-
# @Author: caolinming
# @Date:   2017-09-18 17:16:39
# @Last Modified by:   caolinming
# @Last Modified time: 2017-09-19 09:04:36
# 分布式 工作进程

import time, sys, Queue
from multiprocessing.managers import BaseManager

# 创建 类似的 QueueManager:
class QueueManager(BaseManager):
	pass

# 由于这个QueueManager只从网络上获取 Queue， 所以注册时只提供名字
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')

#连接到服务器，也就是运行 taskmanager.py 的机器
server_addr = '127.0.0.1'
print ('Connect to server %s...' % server_addr)

# 端口和验证码注意保持 与 taskmanager.py 设置的完全一致
m = QueueManager(address=(server_addr, 5000), authkey='abc')
# 从网络连接:
m.connect()

# 获取Queue的对象:
task = m.get_task_queue()
result = m.get_result_queue()

# cong task队列取任务，并把结果写入result 队列
for i in range(10):
	try:
		n = task.get(timeout=1)
		print('run task %d * %d...' % (n, n))
		r = '%d * %d = %d' % (n, n, n*n)
		time.sleep(1)
		result.put(r)
	except Queue.Empty:
		print('task queue is empty.')

# 处理结束：
print('worker exit.')
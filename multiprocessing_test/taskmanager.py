# -*- coding: utf-8 -*-
# @Author: caolinming
# @Date:   2017-09-18 16:46:19
# @Last Modified by:   caolinming
# @Last Modified time: 2017-09-19 10:22:27
# laiyuan:https://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001386832973658c780d8bfa4c6406f83b2b3097aed5df6000
# 分布式多进程程序  管理进程

import random, time, Queue
from multiprocessing.managers import BaseManager

# 发送任务的队列
task_queue = Queue.Queue()
# 接收结果的队列
result_queue = Queue.Queue()

# cong BaseManager 继承的 QueueManager:
class QueueManager(BaseManager):
	pass

# 把两个 Queue 都注册到网络上， callable 参数关联了 Queue 对象：
QueueManager.register('get_task_queue', callable=lambda: task_queue)
QueueManager.register('get_result_queue', callable=lambda: result_queue)

# 绑定端口 5000 ，设置验证码 ‘abc’：
manager = QueueManager(address=('', 5000), authkey='abc')

# 启动Queue:
manager.start()
# 获得通过网络访问的Queue对象:
task = manager.get_task_queue()
result = manager.get_result_queue()

# 放几个任务进去:
for i in range(10):
	n = random.randint(0, 10000)
	print('Put task %d' % n)
	task.put(n)

# 从 result 队列读取结果:
print('Try get results...')
for i in range(10):
	try:
		r = result.get(timeout=10)
		print('Result: %s' % r)
	except Exception,a:
		print "超时"
	except Exception,e:
		print Exception, ":", e


# 关闭：
manager.shutdown()

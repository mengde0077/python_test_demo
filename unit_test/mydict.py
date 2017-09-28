# -*- coding: utf-8 -*-
# @Author: caolinming
# @Date:   2017-09-19 16:38:31
# @Last Modified by:   caolinming
# @Last Modified time: 2017-09-19 16:43:07
# https://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/00140137128705556022982cfd844b38d050add8565dcb9000


class Dict(dict):

	def __init__(self, **kw):
		super(Dict, self).__init__(**kw)

	def __getattr__(self, key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError(r" 'Dict' object has no attribute '%s'" % key)

	def __setattr__(self, key, value):
		self[key] = value

# -*- coding: utf-8 -*-
# @Author: caolinming
# @Date:   2017-09-19 16:43:30
# @Last Modified by:   caolinming
# @Last Modified time: 2017-09-19 17:24:29
# https://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/00140137128705556022982cfd844b38d050add8565dcb9000

import unittest

from mydict import Dict

class TestDict(unittest.TestCase):

	def test_init(self):
		d = Dict(a=1, b='test')
		self.assertEquals(d.a, 1)
		self.assertEquals(d.b, 'test')
		self.assertTrue(isinstance(d, dict))

	def test_key(self):
		d = Dict()
		d['key'] = 'value'
		self.assertEquals(d.key, 'value')

	def test_attr(self):
		d = Dict()
		d.key = 'value'
		self.assertTrue('key' in d)
		self.assertEquals(d['key'], 'value')

	def test_keyerror(self):
		d = Dict()
		with self.assertRaises(KeyError):
			value = d['empty']

	def test_attrerror(self):
		d = Dict()
		with self.assertRaises(AttributeError):
			value = d.empty

if __name__ == '__main__':
	unittest.main()

# -*- coding: utf-8 -*-
# @Author: caolinming
# @Date:   2017-09-19 14:59:41
# @Last Modified by:   caolinming
# @Last Modified time: 2017-09-19 15:12:17

import requests

r = requests.get(url = 'http://www.baidu.com')
print(r.status_code)

r = requests.get(url = 'http://dict.baidu.com/s', params={'wd':'oython'})
print(r.url)   # http://dict.baidu.com/s?wd=oython
# print(r.text)


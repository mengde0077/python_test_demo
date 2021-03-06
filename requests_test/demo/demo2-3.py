# -*- coding: utf-8 -*-
# @Author: caolinming
# @Date:   2017-09-19 14:59:41
# @Last Modified by:   caolinming
# @Last Modified time: 2017-09-19 16:24:16
# http://blog.csdn.net/shanzhizi/article/details/50903748

import requests
import json

url = 'https://m.8dol.com/apkUpdate/judgeClient'
params = {'version_name':'4.0.3','version_code':123}

headers = {'content-type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}


try:
	r = requests.get(url = url, params = params, headers = headers, timeout=1)
	r.raise_for_status()

except requests.Timeout:
	print('请求超时')

except requests.RequestException as e:
	print(e)

else:
	result = r.json()
	print(type(result), result)
	print result['msg']

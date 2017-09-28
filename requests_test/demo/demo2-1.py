# -*- coding: utf-8 -*-
# @Author: caolinming
# @Date:   2017-09-19 14:59:41
# @Last Modified by:   caolinming
# @Last Modified time: 2017-09-19 15:23:25

import requests

url = 'https://m.8dol.com/apkUpdate/judgeClient'

r = requests.get(url = url, params={'version_name':'4.0.3','version_code':123})

# https://m.8dol.com/apkUpdate/judgeClient?version_name=4.0.3&version_code=123
print(r.url)

print(r.text)


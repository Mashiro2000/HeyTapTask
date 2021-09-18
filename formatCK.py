# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/12
# @Author  : 2984922017@qq.com
# @File    : config.py
# @Software: PyCharm
import re

def change(user, CK, UA):
     dic = {}
     dic['user'] = user
     dic['UA'] = UA

     source = re.findall(r'source_type=.*?;', CK)[0]
     tokenID = re.findall(r'TOKENSID=.*?;', CK)[0]
     app_param = re.findall(r'app_param=.*?;', CK)[0]
     if all([source,tokenID,app_param]):
          newCK = source + tokenID
          dic['CK'] = newCK
          dic['app_param'] = app_param
     print(dic)

if __name__ == '__main__':
     user = ''
     CK = ''
     UA = ''
     change(user,CK, UA)
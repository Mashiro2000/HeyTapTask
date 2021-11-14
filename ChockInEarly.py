# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/9/12
# @Author  : MashiroF
# @File    : ChockInEarly.py
# @Software: PyCharm

'''
cron:  35 0,19 * * * ChockInEarly.py
new Env('欢太早睡打卡');
'''

import os
import re
import sys
import time
import random

# 配置文件
try:
    from HT_config import downFlag,notifyBlackList,logger
    import requests
except Exception as error:
    logger.info(f'失败原因:{error}')
    sys.exit(0)

# 判断是否发生下载行为
if downFlag == True:
    logger.info('发生下载行为,应退出程序，编辑配置文件')
    sys.exit(0)

# 配信文件
try:
    from sendNotify import send
except Exception as error:
    logger.info('推送文件有误')
    logger.info(f'失败原因:{error}')
    sys.exit(0)

# 导入账户
try:
    from HT_account import accounts
    lists = accounts
except Exception as error:
    logger.info(f'失败原因:{error}')
    lists = []

# 配信内容格式
allMess = ''
def notify(content=None):
    global allMess
    allMess = allMess + content + '\n'
    logger.info(content)

# 日志录入时间
notify(f"任务:欢太早睡打卡\n时间:{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())}")

class CheckInEarly:
    def __init__(self,dic):
        self.dic = dic
        self.sess = requests.session()

    # 登录验证
    def login(self):
        url = 'https://store.oppo.com/cn/oapi/users/web/member/check'
        headers = {
            'Host': 'store.oppo.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate, br',
        }
        response = self.sess.get(url=url,headers=headers).json()
        if response['code'] == 200:
            notify(f"{self.dic['user']}\t登录成功")
            return True
        else:
            notify(f"{self.dic['user']}\t登录失败")
            return False

    # 报名或打卡
    # 报名或打卡是同一个链接，配合Linux定时系统
    def early(self):
        url = 'https://store.oppo.com/cn/oapi/credits/web/clockin/applyOrClockIn'
        headers = {'Host': 'store.oppo.com',
                   'Connection': 'keep-alive',
                   'source_type': '501',
                   'clientPackage': 'com.oppo.store',
                   'Accept': 'application/json, text/plain, */*',
                   'Referer': 'https://store.oppo.com/cn/app/cardingActivities?us=gerenzhongxin&um=hudongleyuan&uc=zaoshuidaka',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
                   }
        response = self.sess.get(url=url,headers=headers).json()
        if response['code'] == 200:
            if response['data']['clockInStatus'] == 0:
                if response['data']['applyStatus'] == 0:
                    notify(f"{self.dic['user']}\t积分过少，取消报名!")
                elif response['data']['applyStatus'] == 1:
                    notify(f"{self.dic['user']}\t报名成功!")
                elif response['data']['applyStatus'] == 2:
                    notify(f"{self.dic['user']}\t已报名!")
            elif response['data']['clockInStatus'] == 1:
                notify(f"{self.dic['user']}\t早睡瓜分积分，打卡成功!")
            elif response['data']['clockInStatus'] == 2:
                notify(f"{self.dic['user']}\t早睡瓜分积分,已成功打卡!")
        elif response['code'] == 1000005:
            notify(f"{self.dic['user']}\t{response['errorMessage']}")

    # 获取积分数量(只找到这个，找不到昨天积分数据)
    def getIntegral(self):
        url = 'https://store.oppo.com/cn/oapi/credits/web/credits/show'
        headers = {
            'Host': 'store.oppo.com',
            'Connection': 'keep-alive',
            'source_type': '501',
            'clientPackage': 'com.oppo.store',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.9',
            'X-Requested-With': 'com.oppo.store',
            'Referer': 'https://store.oppo.com/cn/app/taskCenter/index?us=gerenzhongxin&um=hudongleyuan&uc=renwuzhongxin'
        }
        response = self.sess.get(url=url,headers=headers).json()
        if response['code'] == 200:
            return f"{self.dic['user']}\t总积分:{response['data']['userCredits']}"
        else:
            return f"{self.dic['user']}\t错误原因:{response}"

    # 执行欢太商城实例对象
    def start(self):
        self.sess.headers.update({
            "User-Agent":self.dic['UA']
        })
        self.sess.cookies.update({
            "Cookie":self.dic['CK']
        })
        if self.login() == True:
            self.early()
            notify(self.getIntegral())
        notify('*' * 40 + '\n')

# 检测CK是否存在必备参数
def checkHT(dic):
    CK = dic['CK']
    if len(re.findall(r'source_type=.*?;',CK)) == 0:
        notify(f"{dic['user']}\tCK格式有误:可能缺少`source_type`字段")
        return False
    if len(re.findall(r'TOKENSID=.*?;',CK)) == 0:
        notify(f"{dic['user']}\tCK格式有误:可能缺少`TOKENSID`字段")
        return False
    if len(re.findall(r'app_param=.*?[;]?',CK)) == 0:
        notify(f"{dic['user']}\tCK格式有误:可能缺少`app_param`字段")
        return False
    return True

# 兼容云函数
def main_handler(event, context):
    global lists
    for each in lists:
        if all(each.values()):
            if checkHT(each):
                checkInEarly = CheckInEarly(each)
                for count in range(3):
                    try:
                        time.sleep(random.randint(2,5))    # 随机延时
                        checkInEarly.start()
                        break
                    except requests.exceptions.ConnectionError:
                        notify(f"{checkInEarly.dic['user']}\t请求失败，随机延迟后再次访问")
                        time.sleep(random.randint(2,5))
                        continue
                else:
                    notify(f"账号: {checkInEarly.dic['user']}\n状态: 取消登录\n原因: 多次登录失败")
                    break
        else:
            notify(f"账号: {each['user']}\n状态: 取消登录\n原因: json数据不齐全")
    if not os.path.basename(__file__).split('_')[-1][:-3] in notifyBlackList:
        send('欢太早睡打卡',allMess)

if __name__ == '__main__':
    main_handler(None,None)

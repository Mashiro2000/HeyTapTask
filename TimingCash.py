# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/9/17
# @Author  : MashiroF
# @File    : TimingCash.py
# @Software: PyCharm

'''
cron:  */30 * * * * TimingCash.py
new Env('欢太定时现金');
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
notify(f"任务:欢太定时现金\n时间:{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())}")

class TimingCash:
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

    # 天天领取现金
    def getDailyCashTask(self):
        url = 'https://store.oppo.com/cn/oapi/omp-web/web/dailyCash/queryActivityReward'
        headers = {
            'Host': 'store.oppo.com',
            'Connection': 'keep-alive',
            'source_type': '501',
            'clientPackage': 'com.oppo.store',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://store.oppo.com/cn/app/cashRedEnvelope?activityId=1&us=shouye&um=xuanfu&uc=xianjinhongbao',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.9'
        }
        params = {
            'activityId':1
        }
        response = self.sess.get(url=url,headers=headers,params=params).json()
        if response['code'] == 200:
            self.timingRewardList = response['data']['timingRewardList']
            return True
        elif response['code'] == 1000001:
            notify(f"[定时红包]\t{response['errorMessage']}")
            return False

    def getCash(self,dic):
        url = 'https://store.oppo.com/cn/oapi/omp-web/web/dailyCash/drawReward'
        headers = {
            'Host': 'store.oppo.com',
            'Connection': 'keep-alive',
            'Origin': 'https://store.oppo.com',
            'source_type': '501',
            'clientPackage': 'com.oppo.store',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://store.oppo.com/cn/app/cashRedEnvelope?activityId=1&us=shouye&um=xuanfu&uc=xianjinhongbao',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.9'
        }
        data = {
            'activityId':1,
            'channel':1,
            'channelRewardId':dic['id']
        }
        response = self.sess.post(url=url,headers=headers,data=data).json()
        if response['code'] == 200:
            notify(f"[定时红包]\t第{dic['id']}个红包:{response['data']['amount']}")
        elif response['code'] == 1000001:
            notify(f"[定时红包]\t第{dic['id']}个红包:{response['errorMessage']}")

    def runtimeReward(self):
        for each in self.timingRewardList:
            if each['hasDraw'] == False:
                self.getCash(dic=each)
                break

    # 执行欢太商城实例对象
    def start(self):
        self.sess.headers.update({
            "User-Agent":self.dic['UA']
        })
        self.sess.cookies.update({
            "Cookie": self.dic['CK']
        })
        if self.login() == True:
            if self.getDailyCashTask() == True:
                self.runtimeReward()
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
        if each['CK']!='' and each['UA'] != '':
            if checkHT(each):
                timingCash = TimingCash(each)
                for count in range(3):
                    try:
                        time.sleep(random.randint(2,5))    # 随机延时
                        timingCash.start()
                        break
                    except requests.exceptions.ConnectionError:
                        notify(f"{timingCash.dic['user']}\t请求失败，随机延迟后再次访问")
                        time.sleep(random.randint(2,5))
                        continue
                else:
                    notify(f"账号: {timingCash.dic['user']}\n状态: 取消登录\n原因: 多次登录失败")
                    break
        else:
            notify(f"账号: {each['user']}\n状态: 取消登录\n原因: json数据不齐全")
    if not os.path.basename(__file__).split('_')[-1][:-3] in notifyBlackList:
        send('欢太定时现金',allMess)

if __name__ == '__main__':
    main_handler(None,None)

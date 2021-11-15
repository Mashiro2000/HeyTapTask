# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/9/26
# @Author  : MashiroF
# @File    : CollectionCard.py
# @Software: PyCharm

'''
cron:  46 5,12 * * * CollectionCard.py
new Env('集卡赢套票');
'''

import os
import re
import sys
import time
import random
import requests

# 配置文件
try:
    from HT_config import downFlag,notifyBlackList,logger
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
notify(f"任务:集卡赢套票\n时间:{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())}")

class CollectionCard:
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

    def drawCard(self):
        url = 'https://store.oppo.com/cn/oapi/credits/web/ccv2/collect'
        headers = {
            "Host": "store.oppo.com",
            "Connection": "keep-alive",
            "s_channel": "oppo_appstore",
            "utm_term": "direct",
            "source_type": "501",
            "utm_campaign": "direct",
            "utm_source": "jika",
            "ut": "direct",
            "uc": "direct",
            "clientPackage": "com.oppo.store",
            "Cache-Control": "no-cache",
            "um": "youshangjiao",
            "ouid": "",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json, text/plain, */*",
            "guid": "",
            "utm_medium": "xidi",
            "appId": "",
            "s_version": "201201",
            "us": "shouye",
            "appKey": "",
            "Origin": "https://store.oppo.com",
            "X-Requested-With": "com.oppo.store",
            "Referer": "https://store.oppo.com/cn/app/collectCard/index?activityId=RWTNLNQ8&us=shouye&um=youshangjiao",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        data = {
            'activityId':'RWTNLNQ8'
        }
        while True:
            response = self.sess.post(url=url,headers=headers,data=data).json()
            if response['code'] == 200:
                notify(f"[集卡活动]\t结果:{response['data']['collectCard']['cardName']}")
            else:
                notify(f"[集卡活动]\t{response['errorMessage']}")
                break
            time.sleep(random.randint(3,5))


    def getTaskList(self):
        url = 'https://store.oppo.com/cn/oapi/credits/web/ccv2/showTaskList?activityId=RWTNLNQ8'
        headers = {
            "Host": "store.oppo.com",
            "Connection": "keep-alive",
            "s_channel": "oppo_appstore",
            "utm_term": "direct",
            "source_type": "501",
            "utm_campaign": "direct",
            "appKey": "",
            "ut": "direct",
            "uc": "direct",
            "clientPackage": "com.oppo.store",
            "Cache-Control": "no-cache",
            "um": "youshangjiao",
            "ouid": "",
            "Accept": "application/json, text/plain, */*",
            "guid": "",
            "appId": "",
            "s_version": "201201",
            "us": "shouye",
            "utm_source": "jika",
            "X-Requested-With": "com.oppo.store",
            "Referer": "https://store.oppo.com/cn/app/collectCard/index?activityId=RWTNLNQ8&us=shouye&um=youshangjiao",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        response = self.sess.get(url=url,headers=headers).json()

        if response['code'] == 200:
            self.taskData = response['data']
            return True
        else:
            notify(f"{response}")
            return False
        time.sleep(random.randint(1,3))

    def runTask(self,dic):
        url = 'https://store.oppo.com/cn/oapi/credits/web/ccv2/ReportedTask'
        params = {
            'activityId':'RWTNLNQ8',
            'taskType':dic['taskId']
        }
        headers = {
            "Host": "store.oppo.com",
            "Connection": "keep-alive",
            "s_channel": "oppo_appstore",
            "utm_term": "direct",
            "source_type": "501",
            "utm_campaign": "direct",
            "appKey": "",
            "ut": "direct",
            "uc": "direct",
            "clientPackage": "com.oppo.store",
            "Cache-Control": "no-cache",
            "um": "youshangjiao",
            "ouid": "",
            "Accept": "application/json, text/plain, */*",
            "guid": "",
            "utm_medium": "xidi",
            "appId": "",
            "s_version": "201201",
            "us": "shouye",
            "utm_source": "jika",
            "X-Requested-With": "com.oppo.store",
            "Referer": "https://store.oppo.com/cn/app/collectCard/index?activityId=RWTNLNQ8&us=shouye&um=youshangjiao",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        response = self.sess.get(url=url,params=params,headers=headers).json()
        if response['code'] == 200:
            notify(f"[{dic['name']}]\t任务完成")
        else:
            notify(f"[{dic['name']}]\tcode:{response['code']}")
        time.sleep(random.randint(3,5))

    def runTaskList(self):
        for each in self.taskData:
            if each['name'] == '每日打卡':
                if each['status'] == 0:
                    self.runTask(dic=each)
                elif each['status'] == 2:
                    notify(f"[{each['name']}]\t已打卡")
            elif each['name'] == '浏览会员日主会场':
                if each['status'] == 0:
                    self.runTask(dic=each)
                elif each['status'] == 2:
                    notify(f"[{each['name']}]\t已浏览")
            elif each['name'] == '分享活动':
                if each['status'] == 0:
                    self.runTask(dic=each)
                elif each['status'] == 2:
                    notify(f"[{each['name']}]\t已浏览")
            elif each['name'] == '浏览会员中心':
                if each['status'] == 0:
                    self.runTask(dic=each)
                elif each['status'] == 2:
                    notify(f"[{each['name']}]\t已浏览")
            elif each['name'] == '浏览秒杀频道':
                if each['status'] == 0:
                    self.runTask(dic=each)
                elif each['status'] == 2:
                    notify(f"[{each['name']}]\t已浏览")
            elif each['name'] == '浏览领券中心':
                if each['status'] == 0:
                    self.runTask(dic=each)
                elif each['status'] == 2:
                    notify(f"[{each['name']}]\t已浏览")

    # 执行欢太商城实例对象
    def start(self):
        self.sess.headers.update({
            "User-Agent":self.dic['UA']
        })
        self.sess.cookies.update({
            "Cookie": self.dic['CK']
        })
        if self.login() == True:
            if self.getTaskList() == True:              # 获取任务中心数据，判断CK是否正确(登录可能成功，但无法跑任务)
                self.runTaskList()                       # 运行任务中心
                self.drawCard()
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
                collectionCard = CollectionCard(each)
                for count in range(3):
                    try:
                        time.sleep(random.randint(2,5))    # 随机延时
                        collectionCard.start()
                        break
                    except requests.exceptions.ConnectionError:
                        notify(f"{collectionCard.dic['user']}\t请求失败，随机延迟后再次访问")
                        time.sleep(random.randint(2,5))
                        continue
                else:
                    notify(f"账号: {collectionCard.dic['user']}\n状态: 取消登录\n原因: 多次登录失败")
                    break
        elif not all(each.values()):
            notify("账号:空账户\t状态:跳过")
        else:
            notify(f"账号: {each['user']}\n状态: 取消登录\n原因: json数据不齐全")
    if not os.path.basename(__file__).split('_')[-1][:-3] in notifyBlackList:
        send('集卡赢套票',allMess)

if __name__ == '__main__':
    main_handler(None,None)

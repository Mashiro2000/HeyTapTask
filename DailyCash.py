# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/9/12
# @Author  : MashiroF
# @File    : DailyCash.py
# @Software: PyCharm

'''
cron:  30 5,12 * * * DailyCash.py
new Env('欢太每日现金');
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
notify(f"任务:欢太每日现金\n时间:{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())}")

class DailyCash:
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

    # 浏览商品
    def viewGoods(self, count,flag,dic=None):
        headers = {
            'clientPackage': 'com.oppo.store',
            'Host': 'msec.opposhop.cn',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'User-Agent': 'okhttp/3.12.12.200sp1',
            'Accept-Encoding': 'gzip'
        }
        result = self.getGoodMess(count=count)    # 秒杀列表存在商品url
        if result['meta']['code'] == 200:
            for each in result['detail']:
                url = f"https://msec.opposhop.cn/goods/v1/info/sku?skuId={each['skuid']}"
                self.sess.get(url=url,headers=headers)
                notify(f"正在浏览商品id:{each['skuid']}...")
                time.sleep(random.randint(7,10))
            if flag == 1:     # 来源天天领现金
                self.getCash(dic=dic)

    # 分享商品
    def shareGoods(self, flag,count,dic=None):
        url = 'https://msec.opposhop.cn/users/vi/creditsTask/pushTask'
        headers = {
            'clientPackage': 'com.oppo.store',
            'Host': 'msec.opposhop.cn',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'User-Agent': 'okhttp/3.12.12.200sp1',
            'Accept-Encoding': 'gzip',
        }
        params = {
            'marking': 'daily_sharegoods'
        }
        for i in range(count + random.randint(1,3)):
            self.sess.get(url=url,headers=headers,params=params)
            notify(f"正在执行第{i+1}次微信分享...")
            time.sleep(random.randint(7,10))
        if flag == 1: #来源天天赚钱
            self.getCash(dic=dic)

    # 秒杀详情页获取商品数据
    def getGoodMess(self,count=10):
        taskUrl = f'https://msec.opposhop.cn/goods/v1/SeckillRound/goods/{random.randint(100,250)}'    # 随机商品
        headers = {
            'clientPackage': 'com.oppo.store',
            'Host': 'msec.opposhop.cn',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'User-Agent': 'okhttp/3.12.12.200sp1',
            'Accept-Encoding': 'gzip',
        }
        params = {
            'pageSize':count + random.randint(1,3)
        }
        response = self.sess.get(url=taskUrl,headers=headers,params=params).json()
        if response['meta']['code'] == 200:
            return response
        else:
            notify(response)

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
            'channel':3,
            'channelRewardId':dic['id']
        }
        response = self.sess.post(url=url,headers=headers,data=data).json()
        if response['code'] == 200:
            notify(f"[{dic['taskName']}]\t{response['data']['amount']}")
        elif response['code'] == 1000001:
            notify(f"[{dic['taskName']}]\t{response['errorMessage']}")

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
            self.taskRewardList = response['data']['taskRewardList']
            self.timingRewardList = response['data']['timingRewardList']
            return True
        elif response['code'] == 1000001:
            notify(response['errorMessage'])
            return False

    # 天天领现金浏览模板
    def viewCashTask(self,dic):
        url = 'https://store.oppo.com/cn/oapi/credits/web/dailyCash/reportDailyTask'
        param = {
            'taskType':dic['taskType'],
            'taskId':f"dailyCash{dic['id']}"
        }
        headers = {
            'Host': 'store.oppo.com',
            'Connection': 'keep-alive',
            'source_type': '501',
            'clientPackage': 'com.oppo.store',
            'Cache-Control': 'no-cache',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://store.oppo.com/cn/app/cashRedEnvelope?activityId=1&us=shouye&um=xuanfu&uc=xianjinhongbao',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.9'
        }
        response = self.sess.get(url=url,headers=headers,params=param).json()
        if response['code'] == 200:
            notify(f"正在执行{dic['taskName']}...")
            time.sleep(random.randint(5,7))
            self.getCash(dic=dic)
        else:
            notify(f"{dic['taskName']}执行失败")


    def runTaskRewardList(self):
        for each in self.taskRewardList:
            if each['taskName'] == '浏览商品':
                if each['taskStatus'] == 0:
                    self.viewGoods(count=6,flag=1,dic=each)
                elif each['taskStatus'] == 1:
                    self.getCash(dic=each)
                elif each['taskStatus'] == 2:
                    notify(f"{each['taskName']}\t已领取")
            elif each['taskName'] == '浏览秒杀专区':
                if each['taskStatus'] == 0:
                    self.viewCashTask(each)
                elif each['taskStatus'] == 1:
                    self.getCash(dic=each)
                elif each['taskStatus'] == 2:
                    notify(f"{each['taskName']}\t已领取")
            elif each['taskName'] == '分享商品':
                if each['taskStatus'] == 0:
                    self.shareGoods(count=2,flag=1,dic=each)
                elif each['taskStatus'] == 1:
                    self.getCash(dic=each)
                elif each['taskStatus'] == 2:
                    notify(f"{each['taskName']}\t已领取")
            elif each['taskName'] == '观看直播':
                if each['taskStatus'] == 0:
                    self.viewCashTask(each)
                elif each['taskStatus'] == 1:
                    self.getCash(dic=each)
                elif each['taskStatus'] == 2:
                    notify(f"{each['taskName']}\t已领取")
            elif each['taskName'] == '浏览签到页':
                if each['taskStatus'] == 0:
                    self.viewCashTask(each)
                elif each['taskStatus'] == 1:
                    self.getCash(dic=each)
                elif each['taskStatus'] == 2:
                    notify(f"{each['taskName']}\t已领取")
            if each['taskName'] == '浏览领券中心':
                if each['taskStatus'] == 0:
                    self.viewCashTask(each)
                elif each['taskStatus'] == 1:
                    self.getCash(dic=each)
                elif each['taskStatus'] == 2:
                    notify(f"{each['taskName']}\t已领取")
            elif each['taskName'] == '浏览realme商品':
                if each['taskStatus'] == 0:
                    self.viewCashTask(each)
                elif each['taskStatus'] == 1:
                    self.getCash(dic=each)
                elif each['taskStatus'] == 2:
                    notify(f"{each['taskName']}\t已领取")
            elif each['taskName'] == '浏览指定商品':
                if each['taskStatus'] == 0:
                    self.viewCashTask(each)
                elif each['taskStatus'] == 1:
                    self.getCash(dic=each)
                elif each['taskStatus'] == 2:
                    notify(f"{each['taskName']}\t已领取")
            elif each['taskName'] == '浏览一加商品':
                if each['taskStatus'] == 0:
                    self.viewCashTask(each)
                elif each['taskStatus'] == 1:
                    self.getCash(dic=each)
                elif each['taskStatus'] == 2:
                    notify(f"{each['taskName']}\t已领取")
            elif each['taskName'] == '浏览OPPO商品':
                if each['taskStatus'] == 0:
                    self.viewCashTask(each)
                elif each['taskStatus'] == 1:
                    self.getCash(dic=each)
                elif each['taskStatus'] == 2:
                    notify(f"{each['taskName']}\t已领取")

    # 执行欢太商城实例对象
    def start(self):
        self.sess.headers.update({
            "User-Agent":self.dic['UA']
        })
        self.sess.cookies.update({
            "Cookie": self.dic['CK']
        })
        if self.login() == True:
            if self.getDailyCashTask() == True:         # 获取天天领现金数据，判断CK是否正确(登录可能成功，但无法跑任务)
                self.runTaskRewardList()                # 运行天天领现金
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
                dailyCash = DailyCash(each)
                for count in range(3):
                    try:
                        time.sleep(random.randint(2,5))    # 随机延时
                        dailyCash.start()
                        break
                    except requests.exceptions.ConnectionError:
                        notify(f"{dailyCash.dic['user']}\t请求失败，随机延迟后再次访问")
                        time.sleep(random.randint(2,5))
                        continue
                else:
                    notify(f"账号: {dailyCash.dic['user']}\n状态: 取消登录\n原因: 多次登录失败")
                    break
        else:
            notify(f"账号: {dailyCash.dic['user']}\n状态: 取消登录\n原因: json数据不齐全")
    if not os.path.basename(__file__).split('_')[-1][:-3] in notifyBlackList:
        send('欢太每日现金',allMess)

if __name__ == '__main__':
    main_handler(None,None)

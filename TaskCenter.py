# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/9/12
# @Author  : MashiroF
# @File    : TaskCenter.py
# @Software: PyCharm

'''
cron:  25 5,12 * * * TaskCenter.py
new Env('欢太任务中心');
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
except:
    lists = []

# 配信内容格式
allMess = ''
def notify(content=None):
    global allMess
    allMess = allMess + content + '\n'
    logger.info(content)

# 日志录入时间
notify(f"任务:欢太任务中心\n时间:{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())}")

# 欢太任务中心类
class TaskCenter:
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

    # 任务中心
    # 位置:我的 -> 任务中心
    # 函数作用:获取任务数据以及判断CK是否正确
    def getTaskList(self):
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
            self.taskData = response['data']
            return True
        else:
            notify(f"{self.dic['user']}\t失败原因:{response['errorMessage']}")
            return False

    # 每日签到
    # 位置: APP → 我的 → 签到
    def signIn(self):
        self.dailyTask()            # 获取签到和每日任务的数据
        if self.signInData['status'] == 0 :
            for each in self.signInData['gifts']:
                if each['today'] == True:
                    url = 'https://store.oppo.com/cn/oapi/credits/web/report/immediately'
                    headers = {
                        'Host': 'store.oppo.com',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Connection': 'keep-alive',
                        'Accept-Language': 'zh-CN,en-US;q=0.9',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'referer':'https://store.oppo.com/cn/app/taskCenter/index'
                    }
                    data = {
                        'amount': each['credits']
                    }
                    while True:
                        response = self.sess.post(url=url, headers=headers,data=data).json()
                        if response['code'] == 200:
                            notify(f"{self.dic['user']}\t签到结果:{response['data']['message']}")
                            break
                        elif response['code'] == 1000005:
                            data = {
                                'amount': each['credits'],
                                'type': each['type'],
                                'gift': each['gift']
                            }
                        else:
                            notify(f"{self.dic['user']}\t签到结果:{response['errorMessage']}")
                            break
        elif self.signInData['status'] == 1:
            notify(f"{self.dic['user']}\t今日已签到")
        else:
            notify(f"{self.dic['user']}\t未知错误")

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

    # 整合每日浏览、分享、推送数据
    def dailyTask(self):
        self.signInData = self.taskData['userReportInfoForm']  # 签到数据源
        for eachTask in self.taskData['everydayList']:          # 每日任务数据源
            if eachTask['marking'] == 'daily_viewgoods':
                self.viewData = eachTask
            elif eachTask['marking'] == 'daily_sharegoods':
                self.shareData = eachTask
            # elif eachTask['marking'] == 'daily_viewpush':
            # self.pushData = eachTask

    # 浏览任务
    def runViewTask(self):
        if self.viewData['completeStatus'] == 0:
            self.viewGoods(count=self.viewData['times'] - self.viewData['readCount'], flag=1)
        elif self.viewData['completeStatus'] == 1:
            self.cashingCredits(self.viewData['name'],self.viewData['marking'], self.viewData['type'],self.viewData['credits'])
        elif self.viewData['completeStatus'] == 2:
            notify(f"[{self.viewData['name']}]\t已完成，奖励已领取")
        time.sleep(random.randint(1,3))


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
            if flag == 1:       # 来源任务中心的浏览任务
                self.cashingCredits(self.viewData['name'], self.viewData['marking'], self.viewData['type'],self.viewData['credits'])
            elif flag == 2:     # 来源赚积分的浏览任务
                self.receiveAward(dic)

    # 分享任务
    def runShareTask(self):
        if self.shareData['completeStatus'] == 0:
            self.shareGoods(flag=1,count=self.shareData['times'] - self.shareData['readCount'])
        elif self.shareData['completeStatus'] == 1:
            self.cashingCredits(self.shareData['name'],self.shareData['marking'], self.shareData['type'],self.shareData['credits'])
        elif self.shareData['completeStatus'] == 2:
            notify(f"[{self.shareData['name']}]\t已完成，奖励已领取")
            time.sleep(random.randint(1,3))

    # 分享商品
    def shareGoods(self, flag,count):
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
        if flag == 1: # 来源任务中心
            self.cashingCredits(self.shareData['name'],self.shareData['marking'], self.shareData['type'],self.shareData['credits'])


    #     # 浏览推送任务
    #     def runViewPush(self):
    #         if self.pushData['completeStatus'] == 0:
    #             self.viewPush(self.pushData['times'] - self.pushData['readCount'])
    #         elif self.pushData['completeStatus'] == 1:
    #             self.cashingCredits(self.pushData['name'], self.pushData['marking'], self.pushData['type'],self.pushData['credits'])
    #         elif self.pushData['completeStatus'] == 2:
    #             notify(f"[{self.pushData['name']}]\t已完成，奖励已领取")
    #             time.sleep(random.randint(1,3))

    #     # 点击推送
    #     def viewPush(self,count):
    #         url = 'https://msec.opposhop.cn/users/vi/creditsTask/pushTask'
    #         headers = {
    #             'clientPackage': 'com.oppo.store',
    #             'Host': 'msec.opposhop.cn',
    #             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    #             'Content-Type': 'application/x-www-form-urlencoded',
    #             'Connection': 'keep-alive',
    #             'User-Agent': 'okhttp/3.12.12.200sp1',
    #             'Accept-Encoding': 'gzip',
    #         }
    #         params = {
    #             'marking': 'daily_viewpush'
    #         }
    #         for i in range(count + random.randint(1,3)):
    #             self.sess.get(url=url,headers=headers,params=params)
    #             notify(f"正在点击第{i+1}次信息推送...")
    #             time.sleep(random.randint(7,10))
    #         self.cashingCredits(self.pushData['name'], self.pushData['marking'], self.pushData['type'],self.pushData['credits'])

    # 领取奖励
    def cashingCredits(self,name,marking,type,amount):
        url = 'https://store.oppo.com/cn/oapi/credits/web/credits/cashingCredits'
        headers = {
            'Host': 'store.oppo.com',
            'Connection': 'keep-alive',
            'Origin': 'https://store.oppo.com',
            'clientPackage': 'com.oppo.store',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.9',
            'Referer':'https://store.oppo.com/cn/app/taskCenter/index?us=gerenzhongxin&um=hudongleyuan&uc=renwuzhongxin'
        }
        data = {
            'marking':marking,
            'type':str(type),
            'amount':str(amount)
        }
        response = self.sess.post(url=url,headers=headers,data=data).json()
        if response['code'] == 200:
            notify(f'{name}\t已领取奖励')
        else:
            notify(f'{name}\t领取失败')
        time.sleep(random.randint(1,3))

    # 赚积分(抽奖)任务
    def runEarnPoint(self):
        aid = 1418  # 抓包结果为固定值:1418
        url = 'https://hd.oppo.com/task/list'
        headers = {
            'Host':'hd.oppo.com',
            'Connection': 'keep-alive',
            'Referer':'https://hd.oppo.com/act/m/2021/jifenzhuanpan/index.html?us=gerenzhongxin&um=hudongleyuan&uc=yingjifen',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.9',
        }
        params = {
            'aid':aid
        }
        response = self.sess.get(url=url,headers=headers,params=params).json()
        if response['no'] == '200':
            for each in response['data']:
                if each['title'] == '每日签到':
                    if each['t_status'] == 0:
                        self.clockIn(each)
                elif each['title'] == '浏览商详':
                    if each['t_status'] == 0:
                        self.viewGoods(count=6,flag=2,dic=each)
        time.sleep(random.randint(1,3))

    # 赚积分 -> 每日打卡
    def clockIn(self,dic):
        aid = 1418
        url = 'https://hd.oppo.com/task/finish'
        headers = {
            'Host': 'hd.oppo.com',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Origin': 'https://hd.oppo.com',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'https://hd.oppo.com/act/m/2021/2021/realmejifendalu/index.html',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.9'
        }
        data = {
            'aid': aid,
            't_index': dic['t_index']
        }
        response = self.sess.post(url=url,headers=headers,data=data).json()
        if response['no'] == '200':
            notify(f"[{dic['title']}]\t{response['msg']}")
            self.receiveAward(dic)
        else:
            notify(f"[{dic['title']}]\t{response['msg']}")
            time.sleep(random.randint(3,5))

    # 领取奖励
    def receiveAward(self,dic):
        aid = 1418
        url = 'https://hd.oppo.com/task/award'
        headers = {
            'Host': 'hd.oppo.com',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Origin': 'https://hd.oppo.com',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'https://hd.oppo.com/act/m/2021/jifenzhuanpan/index.html?us=gerenzhongxin&um=hudongleyuan&uc=yingjifen',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.9'
        }
        data = {
            'aid': aid,
            't_index': dic['t_index']
        }
        response = self.sess.post(url=url,headers=headers,data=data).json()
        if response['no'] == '200':
            notify(f"[{dic['title']}]\t{response['msg']}")
        else:
            notify(f"[{dic['title']}]\t{response['msg']}")
        time.sleep(random.randint(1,3))

    # 跑任务中心
    # 位置:我的 -> 任务中心
    def runTaskCenter(self):
        self.signIn()              # 签到打卡
        self.runViewTask()          # 浏览任务
        self.runShareTask()         # 分享任务
        self.runEarnPoint()         # 赚积分任务(不抽卡)
        # self.runViewPush()          # 浏览推送任务(已下架)

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
                self.runTaskCenter()                    # 运行任务中心
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
                taskCenter = TaskCenter(each)
                for count in range(3):
                    try:
                        time.sleep(random.randint(2,5))    # 随机延时
                        taskCenter.start()
                        break
                    except requests.exceptions.ConnectionError:
                        notify(f"{taskCenter.dic['user']}\t请求失败，随机延迟后再次访问")
                        time.sleep(random.randint(2,5))
                        continue
                else:
                    notify(f"账号: {taskCenter.dic['user']}\n状态: 取消登录\n原因: 多次登录失败")
                    break
    if not os.path.basename(__file__).split('_')[-1][:-3] in notifyBlackList:
        send('欢太任务中心',allMess)

if __name__ == '__main__':
    main_handler(None,None)

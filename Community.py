# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/11/14
# @Author  : MashiroF
# @File    : Community.py
# @Software: PyCharm

'''
cron:  30 6,12 * * * Community.py
new Env('OPPO社区签到、早起打卡');
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
notify(f"任务:OPPO社区签到、早起打卡\n时间:{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())}")

class Community:
    def __init__(self,dic):
        self.sess = requests.session()
        self.dic = dic
        self.ID = 453509395675611143

    def login(self):
        url = 'https://i-user.oppo.cn/member/v3/index/get.pb'
        headers = {
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive",
            "Host": "i-user.oppo.cn",
            "TAP-GSLB": "0,0",
            "User-Agent": "okhttp/3.12.12.217",
            'Accept': 'application/json, text/plain, */*'
        }
        response = self.sess.get(url=url,headers=headers).json()
        if response['message']['code'] == 200:
            self.loginMess = response
            notify(f"{self.dic['user']}\t登录成功")
            return True
        else:
            notify(f"{self.dic['user']}\t登录失败")
            return False

    # def computerValue(self,c,d):
    #     r = int(d + (random.random() % 10) * 16) % 16 | 0
    #     d = math.floor(d / 16)
    #     return d,hex(r if c == 'x' else (r & 0x3 | 0x8))[-1]
    #
    # def generateUUID(self):
    #     d = round(time.time() * 1000)
    #     oldStr = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'
    #     newStr = ''
    #     for i in oldStr:
    #         if i == 'x' or i == 'y':
    #             d,v = self.computerValue(i,d)
    #             newStr += v
    #         else:
    #             newStr += i
    #     return newStr

    def ClockIn(self):
        url = 'https://i-api.oppo.cn/sign/v1/index/create.pb'
        headers = {
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive",
            "Host": "i-api.oppo.cn",
            "TAP-GSLB": "0,0",
            "User-Agent": "okhttp/3.12.12.217",
            'Accept': 'application/json, text/plain, */*'
        }
        response = self.sess.get(url=url,headers=headers).json()
        if response['message']['code'] == 200 and response['message']['msg'] == '操作成功':
            notify(f"[每日签到]\t签到成功")
        elif response['message']['code'] == 200 and response['message']['msg'] == 'SUCCESS':
            notify(f"[每日签到]\t已签到")
        else:
            notify(f"[每日签到]\t签到失败\t失败原因:{response}")

    def SignUp(self):
        url = 'https://hdapi.oppo.cn/user/attendance/signUp'
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Host": "hdapi.oppo.cn",
            "Origin": "https://hdpage.oppo.cn",
            "Pragma": "no-cache",
            "Referer": f"https://hdpage.oppo.cn/rglpdu/index.html?id={self.ID}",
            "X-Requested-With": "XMLHttpRequest"
        }
        data = {
            'attendanceId':self.ID,
            'nickName':self.loginMess['nickname']
        }
        response = self.sess.post(url=url,headers=headers,data=data).json()
        if response['code'] == 200:
            notify(f"[早起打卡]\t报名成功")
        else:
            notify(f"[早起打卡]\t{response['msg']}")


    def SignIn(self):
        url = 'https://hdapi.oppo.cn/user/attendance/signIn'
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Host": "hdapi.oppo.cn",
            "Origin": "https://hdpage.oppo.cn",
            "Pragma": "no-cache",
            "Referer": f"https://hdpage.oppo.cn/rglpdu/index.html?id={self.ID}",
            "X-Requested-With": "XMLHttpRequest"
        }
        data = {
            'attendanceId':self.ID
        }
        response = self.sess.post(url=url,headers=headers,data=data).json()
        if response['code'] == 200:
            notify(f"[早起打卡]\t打卡成功")
        else:
            notify(f"[早起打卡]\t{response['msg']}")

    def getTime(self):
        now = time.time()
        TZ = time.strftime("%Z", time.localtime(now))
        if TZ == 'UTC' or TZ == '协调世界时':
            return time.strftime('%H:%M:%S',time.localtime(now+ 8*3600))
        elif TZ == 'CST' or TZ == '中国标准时间':
            return time.strftime('%H:%M:%S',time.localtime(now))
        else:
            notify(f"时区设置错误,当前时区:{TZ}\t预期时区:CST")
            return False

    def earlyBed(self):
        now = self.getTime()
        if now != False:
            if now > '09:30:00' and now < '23:59:00':
                self.SignUp()
            elif now > '05:30:00' and now < '09:00:00':
                self.SignIn()
            else:
                notify(f"[早起打卡]\t打卡报名时间段外，取消后续操作")


    def start(self):
        token = re.findall(r'TOKENSID=(.*?;)',self.dic['CK'],re.S)
        if token !=[]:
            self.sess.headers.update({
                "User-Agent":self.dic['UA']
            })
            self.sess.cookies.update({
                "Cookie": ';token=' + token[0]
            })
            if self.login() == True:
                self.ClockIn()
                self.earlyBed ()
            notify('*' * 40 + '\n')

def checkHT(dic):
    if len(re.findall(r'TOKENSID=.*?;',dic['CK'])) == 0:
        notify(f"{dic['user']}\tCK格式有误:可能缺少`TOKENSID`字段")
        return False
    return True

# 兼容云函数
def main_handler(event, context):
    global lists
    for each in lists:
        if each['CK']!='' and each['UA'] != '':
            if checkHT(each):
                community = Community(each)
                for count in range(3):
                    try:
                        time.sleep(random.randint(2,5))    # 随机延时
                        community.start()
                        break
                    except requests.exceptions.ConnectionError:
                        notify(f"{community.dic['user']}\t请求失败，随机延迟后再次访问")
                        time.sleep(random.randint(2,5))
                        continue
                else:
                    notify(f"账号: {community.dic['user']}\n状态: 取消登录\n原因: 多次登录失败")
                    break
        else:
            notify(f"账号: {each['user']}\n状态: 取消登录\n原因: json数据不齐全")
    if not os.path.basename(__file__).split('_')[-1][:-3] in notifyBlackList:
        send('OPPO社区签到、早起打卡',allMess)

if __name__ == '__main__':
    main_handler(None,None)

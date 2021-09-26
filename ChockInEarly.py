# !/usr/bin/env python
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
import logging

# 日志模块
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logFormat = logging.Formatter("%(message)s")

# 日志输出流
stream = logging.StreamHandler()
stream.setFormatter(logFormat)
logger.addHandler(stream)

# 日志录入时间
logger.info(f"任务:{'任务中心'}\n时间:{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())}")

# 第三方库
try:
    import requests
except ModuleNotFoundError:
    print("缺少requests依赖！程序将尝试安装依赖！")
    os.system("pip3 install requests -i https://pypi.tuna.tsinghua.edu.cn/simple")
    os.execl(sys.executable, 'python3', __file__, *sys.argv)

# 检测配置文件是否已下载
if not os.path.exists('HT_config.py'):
    logger.info('配置文件不存在,尝试进行下载...')
    url = 'https://ghproxy.com/https://raw.githubusercontent.com/Mashiro2000/QL_HeyTap/main/HT_config.py'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52'
    }
    configText = requests.get(url=url,headers=headers).content.decode('utf8')
    with open(file= 'HT_config.py',mode='w',encoding='utf-8') as fc:
        fc.write(configText)
    logger.info('下载命令执行完毕!')
    logger.info('请根据导航进行配置')
    logger.info('青龙面板 -> 脚本管理 -> 搜索`HT_config`关键字 -> 编辑')
    sys.exit(0)
    
# 配置文件
try:
    logger.info('尝试导入本地欢太CK...')
    from HT_config import accounts,text
    logger.info(text)
    lists = accounts
except:
    logger.info('本地欢太CK不存在')
    lists = []

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
            logger.info(f"{self.dic['user']}\t登录成功")
            return True
        else:
            logger.info(f"{self.dic['user']}\t登录失败")
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
                    logger.info(f"{self.dic['user']}\t积分过少，取消报名!")
                elif response['data']['applyStatus'] == 1:
                    logger.info(f"{self.dic['user']}\t报名成功!")
                elif response['data']['applyStatus'] == 2:
                    logger.info(f"{self.dic['user']}\t已报名!")
            elif response['data']['clockInStatus'] == 1:
                logger.info(f"{self.dic['user']}\t早睡瓜分积分，打卡成功!")
            elif response['data']['clockInStatus'] == 2:
                logger.info(f"{self.dic['user']}\t早睡瓜分积分,已成功打卡!")
        elif response['code'] == 1000005:
            logger.info(f"{self.dic['user']}\t{response['errorMessage']}")

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
        logger.info('*' * 40 + '\n')

# 检测CK是否存在必备参数
def checkHT(string):
    if len(re.findall(r'source_type=.*?;',string)) == 0:
        logger.info('CK格式有误:可能缺少`source_type`字段')
        return False
    if len(re.findall(r'TOKENSID=.*?;',string)) == 0:
        logger.info('CK格式有误:可能缺少`TOKENSID`字段')
        return False
    if len(re.findall(r'app_param=.*?[;]?',string)) == 0:
        logger.info('CK格式有误:可能缺少`app_param`字段')
        return False
    return True

# # 格式化设备信息Json
# # 由于青龙的特殊性,把CK中的 app_param 转换未非正常格式，故需要此函数
# def transform(string):
#     dic2 = {}
#     dic1 = eval(string)
#     for i in dic1['app_param'][1:-1].split(','):
#         dic2[i.split(':')[0]] = i.split(':')[-1]
#     if dic1['CK'][-1] != ';':
#         dic1['CK'] = dic1['CK'] + ';'
#     dic1['CK'] = dic1['CK'] + f"app_param={json.dumps(dic2,ensure_ascii=False)}"
#     dic1['CK'] = checkHT(dic1['CK'])
#     return dic1

# # 读取青龙CK
# def getEnv(key):
#     lists2 = []
#     logger.info("尝试导入青龙面板CK...")
#     variable = os.environ.get(key)
#     if variable == None:
#         logger.info("青龙面板环境变量 TH_COOKIE 不存在！")
#     else:
#         for each in variable.split('&'):
#             result = transform(each)
#             if result:
#                 lists2.append(result)
#     return lists2

# 兼容云函数
def main(event, context):
    global lists
    for each in lists:
        if all(each.values()):
            if checkHT(each['CK']):
                checkInEarly = CheckInEarly(each)
                for count in range(3):
                    try:
                        time.sleep(random.randint(2,5))    # 随机延时
                        checkInEarly.start()
                        break
                    except requests.exceptions.ConnectionError:
                        logger.info(f"{checkInEarly.dic['user']}\t请求失败，随机延迟后再次访问")
                        time.sleep(random.randint(2,5))
                        continue
                else:
                    logger.info(f"账号: {checkInEarly.dic['user']}\n状态: 取消登录\n原因: 多次登录失败")
                    break

if __name__ == '__main__':
    main(None,None)

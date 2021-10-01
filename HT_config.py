# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/9/12
# @Author  : MashiroF
# @File    : HT_config.py
# @Software: PyCharm

#################################### 以下配置可更改 #########################################
## 云函数/青龙面板 环境变量优先级  >  配置文件 `HT_config` 变量优先级
# 通知黑名单
# 环境变量名:notifyBlack,多个以`&`隔开
notifyBlackList = ['TimingCash','']

###########################################################################################




####################################### 以下配置不要动 #######################################
# 导入系统内置包
import os
import sys
import logging

# 全局变量
downFlag = False        # 下载标志
notifyBlack = None

# 读取通知黑名单以及转盘抽奖环境变量
if "Lottery" in os.environ:
    Lottery = os.environ["Lottery"]
if "notifyBlack" in os.environ:
    notifyBlack = os.environ["notifyBlack"]

# 日志模块
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logFormat = logging.Formatter("%(message)s")

# 日志输出流
stream = logging.StreamHandler()
stream.setFormatter(logFormat)
logger.addHandler(stream)

# 第三方库
try:
    import requests
except ModuleNotFoundError:
    logger.info("缺少requests依赖！程序将尝试安装依赖！")
    os.system("pip3 install requests -i https://pypi.tuna.tsinghua.edu.cn/simple")
    os.execl(sys.executable, 'python3', __file__, *sys.argv)

# 检测配置文件并下载函数
# Ps:云函数可能不适用,该函数语法不够优雅,希望大佬给个优雅方案
def checkFile(urlList):
    for url in urlList:
        fileName = url.split('/')[-1]
        fileUrl = f'https://ghproxy.com/{url}'
        try:
            if not os.path.exists(fileName):
                global downFlag
                downFlag = True
                logger.info(f"`{fileName}`不存在,尝试进行下载...")
                content = requests.get(url=fileUrl).content.decode('utf-8')
                with open(file=fileName, mode='w', encoding='utf-8') as fc:
                    fc.write(content)
        except:
            logger.info(f'请手动下载配置文件`{fileName[:-3]}`到 {os.path.dirname(os.path.abspath(__file__))}')
            logger.info(f'下载地址:{fileUrl}\n')

# 检测必备文件
fileUrlList = [
    'https://raw.githubusercontent.com/Mashiro2000/HeyTapTask/main/sendNotify.py',
    'https://raw.githubusercontent.com/Mashiro2000/HeyTapTask/main/HT_account.py'
]
checkFile(fileUrlList)

## 提示文本
if os.path.exists('/ql/config/auth.json'):
    logger.info("""
鉴于青龙面板会破坏欢太CK格式，尝试修复无效，故建议使用配置文件
该项目不再支持青龙面板`环境变量`添加账号,请将CK转移至配置文件
青龙面板 -> 脚本管理 -> 搜索`HT_account`关键字 -> 编辑
CK最简格式:'source_type=xxx;TOKENSID=xxx;app_param=xxx;'
""")

###########################################################################################

# 任务列表
# 出自:https://github.com/yyzhou94
TurnTableList = [
    {'act_name': '赚积分',
     'aid': 1418,
     'if_task': True,  # 是否有任务
     'referer': 'https://hd.oppo.com/act/m/2021/jifenzhuanpan/index.html',
     'if_draw': True,  # 是否有抽奖活动
     'extra_draw_cookie': 'app_innerutm={"uc":"yingjifen","um":"hudongleyuan","ut":"direct","us":"gerenzhongxin"};app_utm={"utm_source_app":"direct","utm_campaign_app":"direct","utm_term_app":"direct","utm_medium_app":"direct"};',
     'lid': 1307,
     'draw_times': 3,
     'text':'每次扣取0积分'
     },
    {'act_name': '欢太积分大乱斗',
     'aid': 1598,
     'if_task': True,
     'referer': 'https://hd.oppo.com/act/m/2021/huantaishangchengjif/index.html',
     'if_draw': True,  # 已修复抽奖，如不需要抽奖请自行修改为False
     'extra_draw_cookie': 'app_innerutm={"uc":"realmejifendaluandou","um":"icon","ut":"3","us":"realmeshouye"};app_utm={"utm_source_app":"direct","utm_campaign_app":"direct","utm_term_app":"direct","utm_medium_app":"direct"};',
     'lid': 1487,
     'draw_times': 3,
     'text':'每次扣取10积分'
     },
    {'act_name': '欢太积分大乱斗2',
     'aid': 1598,
     'if_task': True,
     'referer': 'https://hd.oppo.com/act/m/2021/huantaishangchengjif/index.html',
     'if_draw': True,  # 已修复抽奖，如不需要抽奖请自行修改为False
     'extra_draw_cookie': 'app_innerutm={"us":"onepluschannel","um":"active","uc":"renwuzhongxin","ut":"direct"};app_utm={"utm_source":"direct","utm_medium":"direct","utm_campaign":"direct","utm_term":"direct"};',
     'lid': 1535,
     'draw_times': 3,
     'text':'每次扣取10积分',
     },
    {'act_name': 'ReamMe宠粉计划1',
     'aid': 1182,
     'if_task': False,  # 该活动没有任务
     'referer': 'https://hd.oppo.com/act/m/2020/realmechannejifendui/index.html',
     'if_draw': True,  # 已修复抽奖，如不需要抽奖请自行修改为False
     'extra_draw_cookie': 'app_innerutm={"uc":"realmechongfenchoujiang","um":"huodongyaofeng","ut":"direct","us":"relmechannel"};app_utm={"utm_source_app":"direct","utm_campaign_app":"direct","utm_term_app":"direct","utm_medium_app":"direct"};',
     'lid': 1347,
     'draw_times': 1,
     'text':'每次扣取10积分'
     },
    {'act_name': 'ReamMe宠粉计划2',
     'aid': 1616,
     'if_task': False,  # 该活动没有任务
     'referer': 'https://hd.oppo.com/act/m/2020/realmechannejifendui/index.html',
     'if_draw': True,  # 已修复抽奖，如不需要抽奖请自行修改为False
     'extra_draw_cookie': 'app_innerutm={"uc":"realmechongfenchoujiang","um":"huodongyaofeng","ut":"direct","us":"relmechannel"};app_utm={"utm_source_app":"direct","utm_campaign_app":"direct","utm_term_app":"direct","utm_medium_app":"direct"};',
     'lid': 1521,
     'draw_times': 1,
     'text': '每次扣取10积分'
     },
    {'act_name': 'ReamMe宠粉计划3',
     'aid': 1616,
     'if_task': False,  # 该活动没有任务
     'referer': 'https://hd.oppo.com/act/m/2020/realmechannejifendui/index.html',
     'if_draw': True,  # 已修复抽奖，如不需要抽奖请自行修改为False
     'extra_draw_cookie': 'app_innerutm={"us":"onepluschannel","um":"active","uc":"renwuzhongxin","ut":"direct"};app_utm={"utm_source":"direct","utm_medium":"direct","utm_campaign":"direct","utm_term":"direct"};',
     'lid': 1503,
     'draw_times': 1,
     'text': '每次扣取10积分'
     },
    {'act_name': '天天积分翻倍',
     'aid': 675,
     'if_task': False,  # 该活动没有任务
     'referer': 'https://hd.oppo.com/act/m/2019/jifenfanbei/index.html',
     'if_draw': True,  # 已修复抽奖，如不需要抽奖请自行修改为False
     'extra_draw_cookie': 'app_innerutm={"uc":"direct","um":"zuoshangjiao","ut":"direct","us":"shouye"};app_utm={"utm_source_app":"direct","utm_campaign_app":"direct","utm_term_app":"direct","utm_medium_app":"direct"};',
     'lid': 1289,
     'draw_times': 3,
     'text':'每次扣取10积分'
     },
    {'act_name': '天天积分翻倍2',
     'aid': 1270,  # 从原作者代码提取，但是没找到活动页面在哪，暂不提供抽奖
     'if_task': False,  # 该活动没有任务
     'referer': 'https://hd.oppo.com/act/m/2019/jifenfanbei/index.html',
     'if_draw': False,  # 暂时关闭抽奖，请手动抽奖
     'extra_draw_cookie': 'app_innerutm={"uc":"direct","um":"zuoshangjiao","ut":"direct","us":"shouye"};app_utm={"utm_source_app":"direct","utm_campaign_app":"direct","utm_term_app":"direct","utm_medium_app":"direct"};',
     'lid': 1431,
     'draw_times': 5,
     },
    {'act_name': 'RealMe积分大乱斗',
     'aid': 1582,
     'if_task': True,  # 该活动没有任务
     'referer': 'https://hd.oppo.com/act/m/2021/2021/realmejifendalu/index.html',
     'if_draw': True,  # 已修复抽奖，如不需要抽奖请自行修改为False
     'extra_draw_cookie': 'app_innerutm={"us":"wode","um":"puka","uc":"renwuzhongxin","ut":"direct"};app_utm={"utm_source":"direct","utm_medium":"direct","utm_campaign":"direct","utm_term":"direct"};',
     'lid': 1554,
     'draw_times': 3,
     'text':'每次扣取5积分'
     },
]

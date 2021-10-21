# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/9/16
# @Author  : MashiroF
# @File    : BattleForRealMe.py
# @Software: PyCharm
import TaskCenter

cron = {
    'TaskCenter': '25 8,13 * * *',
}


def run(taskName: str):
    globals().get(taskName).main_handler(None, None)


def main_handler(event, context):
    if 'TriggerName' in event:
        run(event['TaskCenter'])
    else:
        print("非定时器触发")
        print(event)

if __name__ == '__main__':
    #main_handler(None, None)
    event = {
        "Type": "Timer",
        "TriggerName": "TaskCenter",
        "Time": "2019-02-21T11:49:00Z",
        "Message": "user define msg body"
    }
    # 设置多个定时器触发，定时器名称为对应模块名称
    main_handler(event, None)

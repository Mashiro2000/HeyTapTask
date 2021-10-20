# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import TaskCenter
import BattleForHeyTap
import BattleForRealMe
import ChockInEarly
import DailyCash
import TimingCash
import UserCredit

cron = {
    'TaskCenter': '25 8,13 * * *',
    'BattleForHeyTap': '45 8,14 * * *',
    'BattleForRealMe': '40 8,16 * * *',
    'ChockInEarly': '33 0,20 * * *',
    'DailyCash': '30 7,15 * * * ',
    'TimingCash': '*/30 * * * *',
    'UserCredit': '37 22 * * * '
}


def run(taskName: str):
    globals().get(taskName).main_handler(None, None)


def main_handler(event, context):
    if 'TriggerName' in event:
        run(event['TriggerName'])
    else:
        print("非定时器触发")
        print(event)

if __name__ == '__main__':
    #main_handler(None, None)
    event = {
        "Type": "Timer",
        "TriggerName": "UserCredit",
        "Time": "2019-02-21T11:49:00Z",
        "Message": "user define msg body"
    }
    # 设置多个定时器触发，定时器名称为对应模块名称
    main_handler(event, None)

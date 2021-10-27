# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/10/27
# @Author  : MashiroF
# @File    : index.py
# @Software: PyCharm
from importlib import import_module

def run(taskName: str):
    taskName = import_module(taskName)
    taskName.main_handler(None, None)


def main_handler(event, context):
    task = event['TriggerName'].split('\r\n')
    run(task)

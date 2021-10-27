# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/10/27
# @Author  : MashiroF
# @File    : index.py
# @Software: PyCharm
from importlib import import_module

def main_handler(event, context):
    taskName = import_module(event['TriggerName'])
    taskName.main_handler(None, None)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @XZGUtil    : 2021-01-09 19:36
# @Site    :
# @File    : logger.py
# @Software: PyCharm
"""
装饰器
说明：
前景色            背景色           颜色
---------------------------------------
30                40              黑色
31                41              红色
32                42              绿色
33                43              黃色
34                44              蓝色
35                45              紫红色
36                46              青蓝色
37                47              白色
显示方式           意义
-------------------------
0                终端默认设置
1                高亮显示
4                使用下划线
5                闪烁
7                反白显示
8                不可见
"""
import sys
import datetime
import os
import traceback
from functools import wraps
import time


def logit(func):
    """
    日志输出
    :param func:
    :return:
    """
    @wraps(func)
    def with_logging(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'\033[1;31m {date} \033[0m - \033[4;33m{func.__name__}\033[0m -\033[1;35m 耗时:{"%.4f" %(t2 - t1)}秒\033[0m - \033[1;32m{result}\033[0m')
        return result
    return with_logging


def async_logit(func):
    @wraps(func)
    async def with_logging(*args, **kwargs):
        t1 = time.time()
        result =await func(*args, **kwargs)
        t2 = time.time()
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'\033[1;31m {date} \033[0m - \033[4;33m{func.__name__}\033[0m -\033[1;35m 耗时:{"%.4f" %(t2 - t1)}秒\033[0m - \033[1;32m{result}\033[0m')
        return result
    return with_logging


def conlog(*args):
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    text = ''
    for tx in args:
        text += f"{tx} "
    trc = traceback.extract_stack()[-2]
    filename = trc.filename
    str = lambda: filename.split("\\")[-1] if "\\" in filename else filename.split('/')[-1]
    str = f'\033[1;32m{date} \033[0m | \033[4;31m{str()}\033[0m  | \033[1;33m {trc.name} : {trc.lineno}\033[0m  |  {text}'
    print(str)
    return str

def tt():
    conlog(90)


if __name__ == '__main__':
  tt()

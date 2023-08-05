#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021-01-12 17:38
# @Site    : 
# @File    : netWortUtil.py
# @Software: PyCharm
"""获取本地ip"""
import socket


def get_host_ip():
    """
    查询本机ip地址
    :return:
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

if __name__ == '__main__':
    print(get_host_ip())
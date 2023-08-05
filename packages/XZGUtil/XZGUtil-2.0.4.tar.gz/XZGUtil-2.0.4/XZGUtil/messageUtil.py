#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @XZGUtil    : 2021-01-05 16:10
# @Site    : 
# @File    : messageUtil.py
# @Software: PyCharm
"""
消息类
"""
from postcard import Smtp


smtp = Smtp()
def init_emal(title,message,send_user,user, pwd, smtp_addr='smtp.mxhichina.com', smtp_port=25):
    """
    发送邮件
    :param title: 邮件标题
    :param message:邮件信息
    :param send_user:发送给的邮箱
    :param user:发送者邮箱
    :param pwd:发送者密码
    :param smtp_addr:服务器
    :param smtp_port:端口
    :return:
    """
    @smtp.process(user=user, pwd=pwd, smtp_addr=smtp_addr, smtp_port=smtp_port)
    def send_emil():
        """
        发送邮件
        :param message:
        :return:
        """
        ret = smtp.send_mail(subject=f"{title}", content=f"{message}", receiver=send_user)
        print(ret)
    send_emil()
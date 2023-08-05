#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021-01-12 9:52
# @Site    : 
# @File    : re_xzg.py
# @Software: PyCharm
"""
:re模块
"""
import json
import re


def loads_jsonp(_jsonp):
    """
    解析jsonp数据格式为json
    """
    try:
        return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1))
    except BaseException:
        raise ValueError('Invalid Input')

def replace_str(start_str,end_str,replace_str,str):
    """
    替换指定字符串为指定字符串
    """
    re_formula = f"{start_str}.*?{end_str}"
    result = re.sub(re_formula, f'{replace_str}', str)
    return result

def find_str(start_str,end_str,str):
    """
    查找以XX开头以XX结尾的字符串,返回找到的列表 (包含开头结尾)
    """
    re_formula = f"{start_str}.*?{end_str}"
    result = re.findall(re_formula, str)
    return result

def find_str_cent(start_str,end_str,str):
    """
    查找以XX开头以XX结尾的字符串,返回找到的列表 （不包含开头结尾）
    """
    re_formula = f"{start_str}(.*?){end_str}"
    result = re.findall(re_formula, str)
    return result

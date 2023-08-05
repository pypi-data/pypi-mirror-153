#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @XZGUtil    : 2020-12-23 21:28
# @Site    :
# @File    : timeUtil.py
# @Software: PyCharm
"""
时间类
"""
import datetime
import time
import json
import requests
from dateutil.relativedelta import relativedelta  # 安装 pip install python-dateutil
from retrying import retry


def datetime_toStr(dt: datetime, fm: str = "%Y-%m-%d") -> str:
    """
    把datetime转成字符串
    :param dt: datetime.datetime.now
    :return: '2020-01-01'
    """
    return dt.strftime(fm)


def datetime_toStr_dil(dt: datetime, fm: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    把datetime转成字符串 详细版
    :param dt: datetime.datetime.now
    :return: '2020-01-01'
    """
    return dt.strftime(fm)


def datetime_toChinStr(dt: datetime, fm: str = "%Y年%m月%d日") -> str:
    """
    把datetime转成中文字符串
    :param dt: datetime.datetime.now
    :return: '2020-01-01'
    """
    return dt.strftime(fm)


def datetime_toChinStr_dil(dt: datetime, fm: str = "%Y年%m月%d日 %H时%M分%S秒") -> str:
    """
    把datetime转成字符串 详细版
    :param dt: datetime.datetime.now
    :return: '2020-01-01'
    """
    return dt.strftime(fm)


def datetime_toCustStr(dt: datetime, fmat: str) -> str:
    """
    把datetime转成自定义字符串
    :param dt: datetime.datetime.now
    fmat: "%Y-%m-%d"  "%Y-%m-%d %H:%M:%S" "%Y年%m月%d日" "%Y年%m月%d日 %H时%M分%S秒"
    :return:
    """
    return dt.strftime(fmat)


def get_now_date(fm: str = "%Y-%m-%d"):
    """
    获取今日日期字符串
    :return:  '2020-01-01'
    """
    return datetime.datetime.now().strftime(fm)


def get_now_time(fm: str = "%Y-%m-%d %H:%M:%S"):
    """
    获取现在时间字符串
    :return:  '2020-01-01 15:29:08'
    """
    return datetime.datetime.now().strftime(fm)


def str_toDatetime(str: str, fm: str = "%Y-%m-%d") -> datetime:
    """
    把字符串转成datetime  精确到日
    :param str: '2020-01-01'
    :return:
    """
    return datetime.datetime.strptime(str, fm)


def dil_str_toDatetime(str: str, fm: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """
    把字符串转成datetime 精确到秒
    :param str: '2020-01-01'
    :return:
    """
    return datetime.datetime.strptime(str, fm)


def str_toTimestamp(strTime: str) -> int:
    """
    把字符串转成时间戳形式
    :param strTime:'2020-01-01'
    :return:<class 'int'> 1577808000
    """
    return int(time.mktime(str_toDatetime(strTime).timetuple()))


def timestamp_tostr(stamp: int, fm: str = "%Y-%m-%d") -> str:
    """
    把时间戳转成字符串形式
    :param stamp: 1577808000
    :return: '2020-01-01'
    """
    return time.strftime(fm, time.localtime(stamp))


def ts_toStr_det(stamp: int, fm: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    把时间戳转成字符串形式精确到秒
    :param stamp: 1577808000
    :return: '2020-01-01'
    """
    return time.strftime(fm, time.localtime(stamp))


def datetime_toTimestamp(dateTime: datetime):
    """
    把datetime类型转时间戳形式
    :param dateTime:datetime.datetime.now()
    :return:<class 'int'> 1608731584
    """
    return int(time.mktime(dateTime.timetuple()))


def str_totime_dil(str_p: str, fm: str = "%Y-%m-%d %H:%M:%S"):
    """时间字符串转换成时间类型"""
    """2019-01-30 15:29:08"""
    dateTime_p = datetime.datetime.strptime(str_p, fm)
    return dateTime_p


def str_totime(str_p: str, fm: str = "%Y-%m-%d"):
    """时间字符串转换成时间类型"""
    """2019-01-30"""
    dateTime_p = datetime.datetime.strptime(str_p, fm)
    return dateTime_p


def substract_Time_dil(dateStr1: str, dateStr2: str) -> datetime:
    """
        返回两个日期之间的差
        :param dateStr1:'2019-01-30 15:29:08'
        :param dateStr2:'2019-01-30 15:29:08'
        :return:<class 'datetime.timedelta'> 60 days, 0:00:00
    """
    str1 = str_totime_dil(dateStr1)
    str2 = str_totime_dil(dateStr2)
    difference = (str2 - str1)
    return {'day': difference.days, 'min': difference.seconds / 60, 'seconds': difference.seconds}


def substract_DateTime(dateStr1: str, dateStr2: str) -> datetime:
    """
    返回两个日期之间的差
    :param dateStr1:'2020-01-01'
    :param dateStr2:'2020-01-01'
    :return:<class 'datetime.timedelta'> 60 days, 0:00:00
    """
    d1 = str_toDatetime(dateStr1)
    d2 = str_toDatetime(dateStr2)
    return d2 - d1


def substract_TimeStamp(dateStr1: str, dateStr2: str) -> int:
    """
     两个日期的 timestamp 差值
    :param dateStr1: '2020-01-01'
    :param dateStr2: '2020-02-01'
    :return: <class 'int'> -5184000
    """
    ts1 = str_toTimestamp(dateStr1)
    ts2 = str_toTimestamp(dateStr2)
    return ts1 - ts2


def compare_dateTime(dateStr1: str, dateStr2: str) -> bool:
    """
    两个日期的比较, 当然也可以用timestamep方法比较,都可以实现
    :param dateStr1:'2020-01-01'
    :param dateStr2:'2020-01-02'
    :return:<class 'bool'> False
    """
    date1 = str_toDatetime(dateStr1)
    date2 = str_toDatetime(dateStr2)
    return date1.date() > date2.date()


def dateTime_Add(dateStr: str, days=0, hours=0, minutes=0) -> datetime:
    """
    指定日期加上 一个时间段，天，小时，或分钟之后的日期
    :param dateStr:'2020-01-01'
    :param days:1
    :param hours:1
    :param minutes:1
    :return:<class 'datetime.datetime'> 2020-01-02 01:01:01
    """
    date1 = dil_str_toDatetime(dateStr)
    return date1 + datetime.timedelta(days=days, hours=hours, minutes=minutes)


def date_time_subtraction(dateStr: str, days=0, hours=0, minutes=0) -> datetime:
    """
    指定日期减去 一个时间段，天，小时，或分钟之后的日期
    :param dateStr:'2020-01-01'
    :param days:1
    :param hours:1
    :param minutes:1
    :return:<class 'datetime.datetime'> 2020-01-02 01:01:01
    """
    date1 = dil_str_toDatetime(dateStr)
    return date1 - datetime.timedelta(days=days, hours=hours, minutes=minutes)


def month_get(date: datetime):
    """
    返回上个月第一个天和最后一天的日期时间
    date:datetime
    :return
    date_from: 2016-01-01 00:00:00
    date_to: 2016-01-31 23:59:59
    """
    dayscount = datetime.timedelta(days=date.day)
    dayto = date - dayscount
    date_from = datetime.datetime(dayto.year, dayto.month, 1, 0, 0, 0)
    date_to = datetime.datetime(dayto.year, dayto.month, dayto.day, 23, 59, 59)
    return date_from, date_to


def format_nowtime_millisecond() -> int:
    """
    获取毫秒级时间戳
    :return:<class 'int'> eg:1608730762129
    """
    t = time.time()
    nowTime = int(round(t * 1000))
    return nowTime


def get_week_day(date: datetime):
    """
    根据日期返回星期几
    :param date:
    :return:
    """
    week_day_dict = {
        0: '星期一',
        1: '星期二',
        2: '星期三',
        3: '星期四',
        4: '星期五',
        5: '星期六',
        6: '星期日',
    }
    day = date.weekday()
    return week_day_dict[day]


def getBetweenDay(begin_date: str, end_date: str) -> list:
    """
    返回两个时间之间的日期列表
    :param begin_date:'2020-01-01'
    :param end_date:'2020-01-05'
    :return:<class 'list'> ['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-01-05']
    """
    date_list = []
    try :
        begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    except:
        begin_date = datetime.datetime.strptime(begin_date.split(' ')[0], "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date.split(' ')[0], "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list


def get_month_b_e_day(month='202001'):
    """传入月份返回当前月份的起始终止日期"""
    year = month[0:4]
    mon = month[4:]
    mon = f'{int(mon) + 1}'
    next_month = int(year + mon)
    # print(next_month)
    if (next_month % 100 == 13):
        next_month = next_month - 12 + 100
    month_end_day = (datetime.datetime(int(str(next_month)[0:4]), int(str(next_month)[4:6]), 1) - datetime.timedelta(
        days=1)).strftime("%Y-%m-%d")
    month_begin_day = month_end_day.rsplit('-', 1)[0] + '-01'
    return month_begin_day, month_end_day


def month_datelist(start_day):
    """
    传入月份，会生成当前月份到传入月份之间的所有月份的开始终止日期
    :param start_day:'2020-01'
    :return:[['2020-01-01', '2020-01-31'], ['2020-02-01', '2020-02-29'], ['2020-03-01', '2020-03-31']]
    """
    start_day = datetime.datetime.strptime(start_day, r"%Y-%m")
    end_day = datetime.datetime.now() - relativedelta(months=1)
    months = (end_day.year - start_day.year) * 12 + end_day.month - start_day.month
    month_range = ['%s%s' % (start_day.year + mon // 12, mon % 12 + 1)
                   for mon in range(start_day.month - 1, start_day.month + months)]
    month_list = []
    for nonth in month_range:
        month_begin_day, month_end_day = get_month_b_e_day(nonth)
        month_list.append([month_begin_day, month_end_day])
    return month_list


def getdate(beforeOfDay: int):
    """
    获取前1天或N天的日期，beforeOfDay=1：前1天；beforeOfDay=N：前N天
    :param beforeOfDay:
    :return:
    """
    today = datetime.datetime.now()
    # 计算偏移量
    offset = datetime.timedelta(days=-beforeOfDay)
    # 获取想要的日期的时间
    re_date = (today + offset).strftime('%Y-%m-%d')
    return re_date


def getBeforeWeekDays(weeks=1):
    """
    获取前一周的所有日期(weeks=1)，获取前N周的所有日期(weeks=N)
    :param weeks:
    :return:
    """
    # 0,1,2,3,4,5,6,分别对应周一到周日
    week = datetime.datetime.now().weekday()
    days_list = []
    start = 7 * weeks + week
    end = week
    for index in range(start, end, -1):
        day = getdate(index)
        print(day)
        days_list.append(day)
    return days_list


def monitoring_run_time(f):
    """
    装饰器
    记录方法运行时间
    :param f:
    :return:
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = f(*args, **kwargs)
        end_time = time.time()
        print("%s执行成功，用时:%.2f" % (f.__name__, end_time - start_time))
        return res

    return wrapper


def judge_time(ti: str, st: str, en: str, year:bool=True):
    """
    字段格式：0000-00-00 00:00:00
    判断时间ti是否在be和en之间，返回True或False
    :param ti: 判断时间
    :param st: 范围开始时间
    :param en: 范围结束时间
    :return: True or  False
    """
    if year:
        d_time_st = datetime.datetime.strptime(st, '%Y-%m-%d %H:%M:%S')
        d_time_en = datetime.datetime.strptime(en, '%Y-%m-%d %H:%M:%S')
        n_time = datetime.datetime.strptime(ti, '%Y-%m-%d %H:%M:%S')
    else:
        d_time_st = datetime.datetime.strptime(st, '%H:%M:%S')
        d_time_en = datetime.datetime.strptime(en, '%H:%M:%S')
        n_time = datetime.datetime.strptime(ti, '%H:%M:%S')
    assert d_time_en > d_time_st, "时间范围需结束时间大于开始时间！"
    if n_time > d_time_st and n_time < d_time_en:
        return True
    else:
        return False


@retry(stop_max_attempt_number=10)
def get_taobao_time():
    """获取在线时间{"sysTime2":"2021-01-12 16:41:50","sysTime1":"20210112164150"}"""
    try:
        url = 'http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp'
        ts = requests.get(url)
        if '调用成功' in ts.text:
            json_data = ts.json()
            return {"sysTime3": ts_toStr_det(json_data.get('data').get('t')),
                    "sysTime2": timestamp_tostr(json_data.get('data').get('t')),
                    "sysTime1": f"{json_data.get('data').get('t')}"}
        else:
            json_data = {"sysTime3": ts_toStr_det(int(time.time())),
                         "sysTime2": datetime_toStr(datetime.datetime.now()),
                         "sysTime1": f"{datetime_toTimestamp(datetime.datetime.now())}"}
            return json_data
    except:
        json_data = {"sysTime3": ts_toStr_det(int(time.time())),
                     "sysTime2": datetime_toStr(datetime.datetime.now()),
                     "sysTime1": f"{datetime_toTimestamp(datetime.datetime.now())}"}
        return json_data


def split_time_h(start_time: str, end_time: str):
    """
    将给定的时间按小时拆分
    :param start_time: %Y-%m-%d %H:%M:%S
    :param end_time: %Y-%m-%d %H:%M:%S
    :return:
    """
    hour_list = []
    date_list = getBetweenDay(start_time, end_time)
    for day in date_list:
        for hour in range(24):
            day_hour = f"{day} {hour:02d}:00:00"
            hour_list.append(day_hour)
    return hour_list


if __name__ == '__main__':
    # now_time = get_now_time("%H:%M:%S")
    # print(now_time)
    # flag = judge_time(now_time, "02:00:00", "05:00:00", year=False)
    # print(flag)
    print(split_time_h("2022-03-05 16:41:50", "2022-03-13 16:41:50"))

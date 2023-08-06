# -*- coding: UTF-8 -*-

import datetime
import time

from common_utils import rand_utils


def compute_interval_days(interval_days, input_time=None):
    """
    @:param: interval_days(int), input_time(datetime.datetime.now())
    计算指定时间在间隔天数后的时间, 如果未传入指定时间则以当前时间为准。
    @:return "yyyy-mm-dd"
    example:
        now-time: 2019-08-06
        compute_interval_days(-3) ==> 2019-08-03
        compute_interval_days(3) ==> 2019-08-09
        compute_interval_days(3, datetime.datetime(2019, 8, 3)) ==> 2019-07-31
    """

    if not input_time:
        input_time = datetime.date.today()
    else:
        if isinstance(input_time, datetime.date):
            pass
        else:
            raise Exception("传入时间类型错误, 应该为 datetime.datetime(y, m, d)")

    output_time = input_time + datetime.timedelta(days=int(interval_days))
    return output_time


def compute_time_stamp():
    """
    返回当前时间的毫秒时间戳
    """
    now_time = time.time()
    now_time_stamp = int(round(now_time * 1000))
    return now_time_stamp


def compute_time_delta(interval_time=0):
    """
    返回当前时间之间某个时间段的毫秒时间戳
    @:param: interval_time: 间隔时间（秒）
    """
    now_time = datetime.datetime.now()
    past_time = now_time - datetime.timedelta(seconds=interval_time)
    t_time = time.mktime(past_time.timetuple()) + past_time.microsecond / 1E6
    return int(round(t_time * 1000))


def compute_time(interval=0, time_format="%Y-%m-%d"):
    """
    :param
        interval: 与当前时间的间隔日期
        time_format: 返回结果时间的字符串格式
    :return
        返回当前时间的年月日格式: yyyy-mm-dd
    example: interval = 1表示一天后的时间, -1表示前一天的时间
    """

    if not isinstance(interval, int):
        raise ValueError("input value error, params must be int type")

    now_time = datetime.datetime.now()
    if interval >= 0:
        real_time = now_time + datetime.timedelta(days=interval)
    else:
        real_time = now_time - datetime.timedelta(days=-interval)
    day_str = real_time.strftime(time_format)
    return day_str


def compute_last_week_time(input_time=None, time_format="%Y-%m-%d"):
    """
    :param
        input_time: 指定计算的时间
        time_format: 指定计算时间的字符串格式
    :return start_time, end_time
    根据指定时间查询指定时间上周的开始时间和结束时间 (返回时间为上上周6到上周5的日期)
    返回格式: yyyy-mm-dd, yyyy-mm-dd
    """
    if not input_time:
        input_time = datetime.datetime.now()
    else:
        input_time = change_str_to_datetime(input_time, str_format=time_format)

    # interval_time表示当前时间与本周一的间隔时间
    interval_time = 0 - input_time.weekday()

    # interval_time-3 表示当前时间与上周五的间隔天数
    end_time = input_time - datetime.timedelta(days=(-(interval_time-3)))
    start_time = end_time - datetime.timedelta(days=6)
    # if interval_time >= 0:
    #     end_time = input_time - datetime.timedelta(days=(input_time.weekday() + 3))
    #     start_time = end_time - datetime.timedelta(days=6)
    # else:
    #     end_time = input_time + datetime.timedelta(days=interval_time)
    #     start_time = end_time + datetime.timedelta(days=-6)
    start_time_str = start_time.strftime(time_format)
    end_time_str = end_time.strftime(time_format)
    return start_time_str, end_time_str


def compute_week_time(input_time=None, time_format="%Y-%m-%d"):
    """
    :param
        input_time: 指定计算的时间
        time_format: 指定计算时间的字符串格式
    :return start_time, end_time
    根据指定时间查询指定时间 本周的开始时间和结束时间 (返回时间为上周6到本周5的日期)
    返回格式: yyyy-mm-dd, yyyy-mm-dd
    """
    if not input_time:
        input_time = datetime.datetime.now()
    else:
        input_time = change_str_to_datetime(input_time, str_format=time_format)
    # interval_time 表示距离本周5的间隔
    interval_time = 4 - input_time.weekday()
    if interval_time >= 0:
        end_time = input_time + datetime.timedelta(days=interval_time)
        start_time = end_time - datetime.timedelta(days=6)
    else:
        end_time = input_time - datetime.timedelta(days=-interval_time)
        start_time = end_time - datetime.timedelta(days=6)
    start_time_str = start_time.strftime(time_format)
    end_time_str = end_time.strftime(time_format)
    return start_time_str, end_time_str


def compute_next_week_first_day(input_time=None, time_format="%Y-%m-%d"):
    """
    :param
        input_time: 指定计算的时间
        time_format: 指定计算时间的字符串格式
    :return day_time
    根据指定时间计算指定时间下周的第一天
    返回格式: yyyy-mm-dd
    """
    if not input_time:
        input_time = datetime.datetime.now()
    else:
        input_time = change_str_to_datetime(input_time, str_format=time_format)
    interval_time = 7 - input_time.weekday()
    first_day_time = input_time + datetime.timedelta(days=interval_time)
    first_day_time_str = first_day_time.strftime(time_format)

    return first_day_time_str


def change_str_to_datetime(input_time=None, str_format="%Y-%m-%d"):
    """
    :param input_time: 指定需要转换的时间, 默认当前时间 "2019-08-09"
    :param str_format: 字符时间的格式, 默认%Y-%m-%d
    :return:
    """
    try:
        spec_time = input_time or change_datetime_to_str(str_format=str_format)
        return datetime.datetime.strptime(spec_time, str_format)
    except Exception as e:
        raise Exception("类型转换失败, 错误信息: e" % e)


def change_datetime_to_str(input_time=None, str_format="%Y-%m-%d"):
    """
    :param input_time: 指定需要转换的时间, 默认当前时间
    :param str_format: 字符时间的格式, 默认%Y-%m-%d
    :return:
    """
    spec_time = input_time or datetime.datetime.now()
    return spec_time.strftime(str_format)


def compute_interval_day(input_time):
    """
    传入指定时间，计算与当前时间与传入时间之间的间隔天数
    :param input_time
    type: str, format: "%Y-%m-%d"
    """
    now_time = datetime.datetime.now()
    day_format = "%Y-%m-%d"

    end_time_str = now_time.strftime(day_format)
    start_time_str = input_time.strftime(day_format)

    end_sec = time.mktime(time.strptime(end_time_str, day_format))
    start_sec = time.mktime(time.strptime(start_time_str, day_format))

    work_days = int((end_sec - start_sec) / (24 * 60 * 60))
    return work_days


def compute_timestamp(time_str, time_format):
    """
    返回指定时间的时间戳, 返回时间戳(精度秒)
    """
    return int(time.mktime(datetime.datetime.strptime(time_str, time_format).timetuple()))


def compute_interval_time(start_time, end_time, time_format="%Y-%m-%d"):
    """
    计算两个时间之间的间隔(精度秒)
    :param start_time:
    :param end_time:
    :param time_format:
    :return:
    """
    if type(start_time) != type(end_time):
        raise ValueError("params type was different, start_time: %s end_time:%s " % (type(start_time), type(end_time)))

    if isinstance(start_time, datetime.datetime) and isinstance(end_time, datetime.datetime):
        start_time_date, end_time_date = start_time, end_time
    elif isinstance(start_time, str) and isinstance(end_time, str):
        start_time_date = change_str_to_datetime(start_time, time_format)
        end_time_date = change_str_to_datetime(end_time, time_format)
    else:
        raise ValueError("params type was error, start_time: %s end_time:%s, type must be: 'str' or 'datetime.datetime'"
                         % (type(start_time), type(end_time)))

    interval_time = (end_time_date - start_time_date).total_seconds()
    return interval_time


def compute_seconds_specific_time(input_time=None, time_format="%Y%m%d%H%M%S"):
    """
    按指定字符模板返回指定时间的字符串格式, 返回时间戳(精度秒)
    """
    if not input_time:
        input_time = datetime.datetime.now()
        specific_time = change_datetime_to_str(input_time=input_time, str_format=time_format)
    else:
        if isinstance(input_time, str):
            specific_time = input_time + str(rand_utils.random_int(min_value=100000, max_value=999999))
        elif isinstance(input_time, datetime.datetime):
            specific_time = change_datetime_to_str(input_time=input_time, str_format=time_format)
        else:
            raise Exception("input_time type error, maybe str or datetime.datetime")

    return specific_time


def compute_special_time_timestamp(input_time, time_format="%Y-%m-%d %H:%M:%S"):
    """
    按指定格式的时间的字符串入参, 返回它的时间戳(精度毫秒)
    """
    if not input_time:
        input_time = datetime.datetime.now()
    else:
        if isinstance(input_time, str):
            input_time = change_str_to_datetime(input_time, time_format)

    return int(round(input_time.timestamp() * 1000))


if __name__ == '__main__':
    # print(compute_interval_days(-3))
    # print(compute_interval_days(-3, datetime.datetime(2019, 8, 3, 15, 0, 0)))
    # a.compute_interval_days(-3)
    # print(DateComputeUtil.compute_time_stamp())
    # print(DateComputeUtil.compute_time_delta(60))
    # print(DateComputeUtil.compute_time_delta(0))
    # print(DateComputeUtil.compute_time())
    # print(compute_last_week_time())
    # print(compute_week_time())
    # print(DateComputeUtil.compute_interval_day(datetime.datetime(2019,7,1,10,30,30)))
    # print()
    # print(change_datetime_to_str())
    # print(change_str_to_datetime())
    # print(compute_week_time())
    # print(compute_last_week_time())
    # print(compute_time_stamp())
    # print(compute_seconds_specific_time("20191112"))
    print(compute_seconds_specific_time())

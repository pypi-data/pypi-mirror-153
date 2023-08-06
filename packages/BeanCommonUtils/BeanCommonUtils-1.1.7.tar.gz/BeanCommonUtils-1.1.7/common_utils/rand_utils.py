# -*- coding: UTF-8 -*-

import random
import string


def random_special_char(length=5):
    """
    '\'', '\"', '&', '\\', '\n', '\r', '\t', '\b', '\f', '\<', '\>',
    '<br/>', '`', '@', '$', '*', '^', '#', '?', '_', '&&'
    随机返回指定长度的上述特殊字符串
    """

    # 16进制
    char_0x = str(
        bytes([0x60, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2a, 0x2b, 0x2c, 0x2d,
               0x2e, 0x2f, 0x3c, 0x3e, 0x3f, 0x40, 0x5b, 0x5c, 0x5d, 0x5e, 0x5f, 0x7b, 0x7c, 0x7d, 0x7e, 0x60]))
    return ''.join(random.sample(char_0x, length))


def random_float_num(max_value=1000, point_num=2):
    return round(random.uniform(1, max_value), point_num)


def random_str(length=8):
    rnd_str = ''.join(random.sample(
        string.ascii_letters + string.digits, length))
    return rnd_str


def random_letters(length=8):
    rnd_str = ''.join(random.sample(string.ascii_letters, length))
    return rnd_str


def random_mobile():
    # 第二位数字
    second = [3, 4, 5, 7, 8][random.randint(0, 4)]

    # 第三位数字
    third = {
        3: random.randint(0, 9),
        4: [5, 7, 9][random.randint(0, 2)],
        5: [i for i in range(10) if i != 4][random.randint(0, 8)],
        7: [i for i in range(10) if i not in [4, 9]][random.randint(0, 7)],
        8: random.randint(0, 9),
    }[second]

    # 最后八位数字
    suffix = random.randint(9999999, 100000000)

    # 拼接手机号
    return "1{}{}{}".format(second, third, suffix)


def random_int(min_value=0, max_value=10000):
    return random.randint(min_value, max_value)


def random_birth(year=None, month=None, day=None):
    year = year or random_int(1991, 2005)
    month = month or random_int(1, 9)
    day = day or random_int(10, 28)
    return "%s-0%s-%s" % (str(year), str(month), str(day))


if __name__ == '__main__':
    print(random_special_char(6))

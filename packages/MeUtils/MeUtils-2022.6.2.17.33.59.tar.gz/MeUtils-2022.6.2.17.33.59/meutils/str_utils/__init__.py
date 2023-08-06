#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : __init__.py
# @Time         : 2022/5/12 下午2:02
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from idna import unichr

from meutils.pipe import *
from meutils.str_utils.translater import translater
from meutils.request_utils.crawler import Crawler

"""todo
url 拼接

"""


def half2all(ustring):
    """半角转全角"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 32:  # 半角空格直接转化
            inside_code = 12288
        elif 32 <= inside_code <= 126:  # 半角字符（除空格）根据关系转化
            inside_code += 65248
        rstring += chr(inside_code)
    return rstring


def all2half(all_string):
    """全角转半角"""
    half_string = ""
    for char in all_string:
        inside_code = ord(char)
        if inside_code == 12288:  # 全角空格直接转换,全角和半角的空格的Unicode值相差12256
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化,除空格外的全角和半角的Unicode值相差65248
            inside_code -= 65248

        half_string += unichr(inside_code)
    return half_string


def to_hump(string="a_b c", pattern='_| '):
    """驼峰式转换"""
    reg = re.compile(pattern)
    _ = reg.sub('', string.title())
    return _.replace(_[0], _[0].lower())


def str_replace(s: str, dic: dict):
    """多值替换
        str_replace('abcd', {'a': '8', 'd': '88'})
    """
    return s.translate(str.maketrans(dic))


def unquote(s='%E6%9C%80%E6%96%B0%E6%9C%8D%E5%8A%A1'):
    """http字符串解码"""
    from urllib import parse

    return parse.unquote(s)


@lru_cache()
def arabic2chinese(arabic=123):
    c = Crawler(f'https://szjrzzwdxje.bmcx.com/{arabic}__szjrzzwdxje')
    return c.xpath('//span//text()')[-3:-1]


@lru_cache(1024)
def json_loads(s):
    if isinstance(s, bytes):
        s = s.decode()
    try:
        return json.loads(s.replace("'", '"'))

    except Exception as e:
        logger.warning(e)

        return eval(s)


if __name__ == '__main__':
    # print(str_replace('abcd', {'a': '8', 'd': '88'}))
    # print(unquote())
    # print(arabic2chinese())
    # print(to_hump())
    # print(translater())

    print(json_loads("{1: 1}"))

# !/usr/bin/env python3.9
# -*-coding:utf-8 -*-

"""
# Author   : Sunny
# @Time    : 2021/8/16 4:09 pm
# @File    : constants.py
# @Software: PyCharm
# desc: 用于定义业务状态代码

使用区间:
200         # 正常返回
10000~19999 # 客户端错误
20000~29999 # 第三方错误
30000~39999 # 程序内部错误
40000~49999 # 其他

"""
DEFAULT_UNKNOWN_EN_MSG = "internal error"
DEFAULT_UNKNOWN_CN_MSG = "程序内部错误，请提交工单处理"

# 正常
OK_CODE = 200
OK_EN_MESSAGE = "success"
OK_CN_MESSAGE = "成功"

# 客户端错误
PARAMETER_ERROR_CODE = 10000
AUTHENTICATION_ERROR_CODE = 100001

# 程序内部错误
UNKNOWN_EXCEPTION_CODE = 30000



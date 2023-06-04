# !/usr/bin/env python3.9
# -*-coding:utf-8 -*-

"""
# Author   : Sunny
# @Time    : 2021/8/16 1:38 pm
# @File    : exceptions.py
# @Software: PyCharm
"""
from typing import Optional
from fastapi import status

from yeti.exceptions import constants


class ErrorBase(Exception):
    business_code: Optional[int] = constants.UNKNOWN_EXCEPTION_CODE
    http_code: Optional[int] = status.HTTP_500_INTERNAL_SERVER_ERROR
    msg_en: Optional[str] = constants.DEFAULT_UNKNOWN_EN_MSG
    msg_cn: Optional[str] = constants.DEFAULT_UNKNOWN_CN_MSG

    def __init__(self, **kwargs):
        self.business_code = (kwargs.get("business_code") or self.business_code)
        self.http_code = (kwargs.get("http_code") or self.http_code)
        try:
            self.msg_cn = (kwargs.get("msg_cn", "") or self.msg_cn) % kwargs
        except KeyError:
            self.msg_cn = kwargs.get("msg_cn", "") or self.msg_cn
        try:
            self.msg_en = (kwargs.get("msg_en", "") or self.msg_en or type(self).__name__) % kwargs
        except KeyError:
            self.msg_en = (kwargs.get("msg_en", "") or self.msg_en or type(self).__name__)
        super(ErrorBase, self).__init__(self.msg_en)

    def json(self):

        return self.__dict__


class ParameterError(ErrorBase):
    """参数错误"""
    msg_cn = "参数 %(parm)s 不合法"
    msg_en = "parameter %(parm)s invalid"
    http_code = status.HTTP_400_BAD_REQUEST
    business_code = constants.PARAMETER_ERROR_CODE


class InternalError(ErrorBase):
    """内部错误"""
    msg_cn = "服务器内部错误，请稍后次尝试！"
    msg_en = "Server internal exceptions. details: %(error_msg)s"
    http_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    business_code = constants.UNKNOWN_EXCEPTION_CODE


class AuthError(ErrorBase):
    """认证失败"""
    msg_cn = "认证失败"
    msg_en = "user %(user_id)s auth fail"
    http_code = status.HTTP_401_UNAUTHORIZED
    business_code = constants.AUTHENTICATION_ERROR_CODE


class SendRequestError(ErrorBase):
    """发送请求失败"""
    msg_cn = "发送请求失败"
    msg_en = "send request error"
    http_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    business_code = constants.UNKNOWN_EXCEPTION_CODE


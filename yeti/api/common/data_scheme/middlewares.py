# !/usr/bin/env python3.9
# -*-coding:utf-8 -*-

"""
# Author   : Sunny
# @Time    : 2021/10/8 9:38 am
# @File    : middlewares.py
# @Software: PyCharm
"""
from typing import Optional, Any
from pydantic import BaseModel

from yeti.exceptions import constants


class HttpLoggingRequestContext(BaseModel):
    client_ip: Optional[str] = ""
    requests_url: Optional[str] = ""
    request_headers: Optional[dict] = ""
    request_method: Optional[str] = ""
    request_body: Optional[Any] = ""


class HttpLoggingResponseContext(BaseModel):
    http_code: Optional[int] = constants.OK_CODE
    business_code: Optional[int] = constants.OK_CODE
    msg_en: Optional[str] = constants.OK_EN_MESSAGE
    msg_cn: Optional[str] = constants.OK_CN_MESSAGE
    details: Optional[str] = ""


class WebsocketRequestContext(BaseModel):
    request_type: Optional[str] = ""
    client_ip_address: Optional[str] = ""
    requests_url: Optional[str] = ""
    request_headers: Optional[dict] = {}


class WebsocketResponseContext(BaseModel):
    http_code: Optional[int] = constants.OK_CODE
    business_code: Optional[int] = constants.OK_CODE
    msg_en: Optional[str] = ""
    msg_cn: Optional[str] = ""
    details: Optional[str] = ""

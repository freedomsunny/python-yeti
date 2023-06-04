# !/usr/bin/env python3.9
# -*-coding:utf-8 -*-

"""
# Author   : Sunny
# @Time    : 2021/11/17 9:43 pm
# @File    : auth_scheme.py
# @Software: PyCharm
"""
from pydantic import BaseModel


class JWTTokenResponse(BaseModel):
    """Jwt token返回数据结构"""
    token: str
    token_type: str = "bearer"


class JWTTokenPayload(BaseModel):
    """Jwt token数据"""
    id: str
    username: str
    email: str
    phone: str


class JWTPasswordAuth(BaseModel):
    username: str
    password: str



# !/usr/bin/env python3.9
# -*-coding:utf-8 -*-

"""
# Author   : Sunny
# @Time    : 2021/9/3 5:50 pm
# @File    : example_data_scheme.py
# @Software: PyCharm
"""
from pydantic import BaseModel
from typing import Optional


class UsersScheme(BaseModel):
    username: str
    age: int
    address: Optional[str] = ""


class ExampleScheme(BaseModel):
    user: UsersScheme
    foo: str
    bar: str

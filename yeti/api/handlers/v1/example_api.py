# !/usr/bin/env python3.9
# -*-coding:utf-8 -*-

"""
# Author   : Sunny
# @Time    : 2021/8/4 3:37 pm
# @File    : example_api.py
# @Software: PyCharm
"""
from fastapi import APIRouter

router = APIRouter(tags=["example"],
                   )


@router.get("/helloword")
async def say_hello():

    return {"result": "hello word"}




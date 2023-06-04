# !/usr/bin/env python3.9
# -*-coding:utf-8 -*-

"""
# Author   : Sunny
# @Time    : 2021/9/15 10:47 pm
# @File    : __init__.py.py
# @Software: PyCharm
"""
from fastapi import FastAPI

app = None


def get_app():
    global app
    if not app:
        app = FastAPI()

    return app

# !/usr/bin/env python3.9
# -*-coding:utf-8 -*-

"""
# Author   : Sunny
# @Time    : 2021/8/23 11:23 am
# @File    : db_api.py
# @Software: PyCharm
关于数据库的API操作，都在这个模块定义
"""
from yeti.db.relational_dbs.models.models import Users
from .DBAPIBase import DBCURDBase


class UsersDBAPI(DBCURDBase):
    """user表"""
    module = Users

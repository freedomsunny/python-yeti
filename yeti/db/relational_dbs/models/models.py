# !/usr/bin/env python3.9
# -*-coding:utf-8 -*-

"""
# Author   : Sunny
# @Time    : 2021/8/23 11:15 am
# @File    : models.py
# @Software: PyCharm
"""
import sqlalchemy as sa

from yeti.db.relational_dbs import ModelsBase


class Users(ModelsBase.BASE):
    """用户表"""
    username = sa.Column(sa.String(64), doc="login user name")
    password = sa.Column(sa.String(256), doc="the hashed password")
    status = sa.Column(sa.Integer, doc="user status")


init_tables_list = [
    Users
]

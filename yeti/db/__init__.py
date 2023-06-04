# !/usr/bin/env python3.9
# -*-coding:utf-8 -*-

"""
# Author   : Sunny
# @Time    : 2021/8/3 5:02 pm
# @File    : __init__.py.py
# @Software: PyCharm
"""
from yeti.db.relational_dbs import init_tables, config_session


config_session()
init_tables()

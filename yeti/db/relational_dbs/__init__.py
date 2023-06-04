# !/usr/bin/env python3.9
# -*-coding:utf-8 -*-

"""
# Author   : Sunny
# @Time    : 2021/8/20 10:14 am
# @File    : __init__.py.py
# @Software: PyCharm
"""

from oslo_db.sqlalchemy import enginefacade
from sqlalchemy.exc import OperationalError

from yeti.db.relational_dbs.models.models import init_tables_list
from yeti.cfg import CONF


def init_tables(tables=init_tables_list):
    """
    自动创建数据库表
    :param tables:
    :return:
    """
    engine = enginefacade.writer.get_engine()
    for table in tables:
        try:
            table.__table__.create(engine)
        # 当表已经存在，会抛出异常
        except OperationalError:
            pass


def config_session(**kwargs):
    kw = {
        "connection": CONF.sql_connection,
        "slave_connection": None,
        "connection_debug": 0,
        "max_pool_size": CONF.connection_poll_size,
    }
    if kwargs:
        kw.update(kwargs)
    enginefacade.configure(**kw)

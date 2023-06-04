# !/usr/bin/env python3.9
# -*-coding:utf-8 -*-

"""
# Author   : Sunny
# @Time    : 2021/8/3 5:37 pm
# @File    : __init__.py.py
# @Software: PyCharm
"""
from yeti.cfg.register_opts import RegisterOptions
from yeti.cfg.options import conf_opts
from oslo_config import cfg


CONF = RegisterOptions.register_opts(opts=conf_opts, conf=cfg.CONF)

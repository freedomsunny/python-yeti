# !/usr/bin/env python3.9
# -*-coding:utf-8 -*-

"""
# Author   : Sunny
# @Time    : 2021/8/12 10:48 am
# @File    : logger.py
# @Software: PyCharm
refer: https://loguru.readthedocs.io/en/stable/api/logger.html
"""
from yeti.cfg import CONF
from loguru import logger as _logger

_config = dict(
    sink=CONF.logging_path,
    level=CONF.logging_level,
    format=CONF.logging_format,
    catch=True,
    enqueue=True,
    colorize=False,
    rotation=CONF.logging_rotation,
    retention=CONF.logging_retention,
    compression="gz",
)


def get_logger_config():
    cfg_kwargs = {}
    for k, v in _config.items():
        if v not in (None, ""):
            cfg_kwargs[k] = v

    return cfg_kwargs


_logger.add(**get_logger_config()
            )

LOG = _logger

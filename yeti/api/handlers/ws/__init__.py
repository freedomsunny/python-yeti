# !/usr/bin/env python3.9
# -*-coding:utf-8 -*-

"""
# Author   : Sunny
# @Time    : 2021/8/12 2:36 pm
# @File    : __init__.py.py
# @Software: PyCharm
"""
from yeti.api.common.ws import WsConnectionManager, WsRedisChannel
from yeti.cfg import CONF

aio_redis = WsRedisChannel(url=CONF.cached_backend)
ws_connector = WsConnectionManager(aio_redis, CONF.websocket_topic)
if CONF.enable_websocket:
    ws_connector.subscribe_ws_channel()



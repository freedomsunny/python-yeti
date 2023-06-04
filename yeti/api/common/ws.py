# !/usr/bin/env python3.9
# -*-coding:utf-8 -*-

"""
# Author   : Sunny
# @Time    : 2021/9/24 2:52 pm
# @File    : ws.py
# @Software: PyCharm
"""
import threading
import json
import asyncio
from typing import List
from fastapi import WebSocket

from yeti.cache.cache import aio_redis
from yeti.utils.utils import SingleInstance
from yeti.log.logger import LOG
from yeti.cache.cache import CacheFactory

mutex = threading.Lock()
# The global user connections per process
active_connections: List[WebSocket] = []


class WsRedisChannel(metaclass=SingleInstance):
    """
    WebSocket redis消息管道类
    """

    def __init__(self, url: str):
        # blocking cache
        self.cache = CacheFactory()
        # none blocking cache
        self.aio_cache = aio_redis(url)
        # 频道对象
        self.channel = self.aio_cache.pubsub()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.channel.close()

    async def unsubscribe(self, channel: str):
        await self.channel.unsubscribe(channel)

    async def subscribe(self, channel: str):
        await self.channel.subscribe(channel)

    async def get_message(self, channel: str, ignore_subscribe_messages: bool = True):
        """
        从redis中获取消息
        :param ignore_subscribe_messages:
        :param channel: 指定要获取频道的信息
        :return:
        """
        message = await self.channel.get_message(ignore_subscribe_messages=ignore_subscribe_messages)
        if message and message["channel"] == channel:
            return message

        return None

    async def publish_message(self, channel: str, message: str):
        """
        发布消息到redis, 只有订阅人数>1的频道才会发布
        :param channel:
        :param message:
        :return:
        """
        subs = dict(await self.aio_cache.pubsub_numsub(channel))
        if subs[channel] >= 1:
            await self.aio_cache.publish(channel, message)


class WsConnectionManager(metaclass=SingleInstance):

    def __init__(self, redis: WsRedisChannel, channel: str):
        self.ws_redis = redis
        self.channel = channel
        self.subscribe_thread = None

    async def connect(self, websocket: WebSocket, message: str = "") -> None:
        """
        新链接
        :param websocket:
        :param message:
        :return:
        """
        await websocket.accept()

        if websocket not in active_connections:
            active_connections.append(websocket)
            if message:
                await self.ws_redis.publish_message(self.channel, message)

    async def disconnect(self, websocket: WebSocket, message: str = ""):
        """
        断开链接
        :param websocket: 断开后需要发送的消息
        :param message:
        :return:
        """
        active_connections.remove(websocket)
        if message:
            await self.ws_redis.publish_message(self.channel, message)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """
        点对点消息
        :param message:
        :param websocket:
        :return:
        """
        await websocket.send_text(message)

    async def broadcast(self, message: str) -> None:
        """
        广播消息本地消息
        :param message:
        :return:
        """
        LOG.info("broadcast message: {}".format(message)
                 )
        for connection in active_connections:
            await connection.send_text(message)

    def subscribe_callback(self, message):
        LOG.info("[ws callback] got websocket message: {} from channel: {}".format(message, self.channel)
                 )
        if isinstance(message, dict):
            message = json.dumps(message)

        asyncio.run(self.broadcast(message))

    def subscribe_ws_channel(self):
        """订阅websocket频道"""
        if self.subscribe_thread:
            LOG.error("Thread {} is running dont call this method twice".format(self.subscribe_thread.getName()
                                                                                ))
            raise RuntimeError("Thread {} is running".format(self.subscribe_thread.getName())
                               )
        self.subscribe_thread = self.ws_redis.cache.cache.subscribe_with_callback(channel=self.channel,
                                                                                  callback=self.subscribe_callback,
                                                                                  run_in_thread=True
                                                                                  )

    def shutdown_subscribe_thread(self) -> None:
        if self.subscribe_thread:
            self.subscribe_thread.stop()

    async def send_message(self, message):
        """
        发送消息
        :param message:
        :return:
        """
        await self.ws_redis.publish_message(self.channel, message)

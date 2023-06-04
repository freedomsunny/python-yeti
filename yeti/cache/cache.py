# -*- coding:utf-8 -*-
import redis
import aioredis

from yeti.cfg import CONF
from yeti.exceptions.exceptions import ParameterError
from yeti.utils.utils import SingleInstance

aio_cache = None


class CacheTypes:
    REDIS = "REDIS"
    MEMCACHED = "MEMCACHED"


class CacheFactory:
    def __init__(self, cache_type=CacheTypes.REDIS, uri=CONF.cached_backend):
        self.cache = None
        cache_type = cache_type.upper()
        if not getattr(CacheTypes, cache_type):
            raise ParameterError
        if cache_type == CacheTypes.REDIS:
            self.cache = RedisBackend(uri=uri)
        # elif cache_type == CacheTypes.MEMCACHED:
        #     self.cache = ""


class RedisBackend(metaclass=SingleInstance):
    """
    doc: https://github.com/andymccurdy/redis-py
    """
    def __init__(self, uri):
        _conn = uri.split("//")[1]
        if '@' in _conn:
            password, host_port = _conn.split('@')
        else:
            password = None
            host_port = _conn
        if password:
            password = password[1:]
        host, db_p = host_port.split(':')
        port, db = db_p.split('/')
        self.conn = redis.StrictRedis(host=host,
                                      port=port,
                                      db=db,
                                      password=password,
                                      decode_responses=True
                                      )

    def get(self, key, default=None, read_delete=False):
        """
        Return object with id 
        """
        result = self.conn.get(key)
        if read_delete:
            try:
                self.conn.delete(key)
            except:
                pass

        return result or default

    def set(self, key, value, timeout=None):
        """
        插入一条数据
        """
        try:
            if value:
                self.conn.set(key, value)
                if timeout:
                    self.conn.expire(key, timeout)
                return True
        except:
            self.conn.delete(key)
            return False

    def delete(self, key):

        self.conn.delete(key)

    def keys(self, key):
        return self.conn.keys(key)

    def lpush(self, key, value):
        """
        向列表增加一个元素
        :param key:
        :param value:
        :return:
        """
        self.conn.lpush(key, value)

    def llen(self, key):
        """
        列表长度
        :return:
        """
        return self.conn.llen(key)

    def lrem(self, key, value, count=0):
        """
        从一个列表中删除某个元素
        :param key:
        :param value:
        :param count:
        count > 0: Remove elements equal to element moving from head to tail.
        count < 0: Remove elements equal to element moving from tail to head.
        count = 0: Remove all elements equal to element.
        :return:
        """
        self.conn.lrem(key, value, count)

    def lrange(self, key, start=0, end=-1):
        """
        获取列表中元素
        :param key:
        :param start:
        :param end:
        :return:
        """

        return self.conn.lrange(key, start, end)

    def subscribe(self, ignore_subscribe_messages=True, *args):
        """
        订阅频道
        :param args: ("channel1", "channel2", "channel3", ...)
        :param ignore_subscribe_messages 是否忽略订阅消息
        :return:
        """
        p = self.conn.pubsub(ignore_subscribe_messages=ignore_subscribe_messages)
        p.subscribe(*args)

        return p

    def publish(self, channel, msg):
        """
        发布消息
        :param channel 频道
        :param msg 发布的消息
        :return:
        """
        self.conn.publish(channel, msg)

    def subscribe_with_callback(self, channel, callback, run_in_thread=False, sleep_time=0.1):
        """订阅某个频道，注册回调函数"""
        p = self.conn.pubsub()
        p.subscribe(**{channel: callback})
        # the event loop is now running in the background processing messages
        # when it's time to shut it down...
        if run_in_thread:
            thread = p.run_in_thread(sleep_time=sleep_time)
            return thread


def aio_redis(url, decode_responses=True, encoding="utf-8"):
    """
    url can one of below:
        redis://[[username]:[password]]@localhost:6379/0
        rediss://[[username]:[password]]@localhost:6379/0
        unix://[[username]:[password]]@/path/to/socket.sock?db=0
    see:
        https://aioredis.readthedocs.io/en/latest/getting-started/
    """
    global aio_cache
    if not aio_cache:
        aio_cache = aioredis.from_url(url,
                                      decode_responses=decode_responses,
                                      encoding=encoding
                                      )

    return aio_cache

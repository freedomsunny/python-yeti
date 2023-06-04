# !/usr/bin/env python3.9
# -*-coding:utf-8 -*-

"""
# Author   : Sunny
# @Time    : 2021/8/9 1:32 pm
# @File    : utils.py
# @Software: PyCharm
"""
import os
import time
import json
import decimal
import datetime
from functools import wraps
from sqlalchemy.ext.declarative import DeclarativeMeta
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Utils:

    @classmethod
    def get_process_numbers(cls):
        """
        get cpu count
        :return:
        """
        return os.cpu_count()

    @classmethod
    def string2timestamp(cls, fmt: str, date_str: str):
        """将时间字符串转换为时间戳
        :param fmt: "%Y-%m-%dT%H:%M:%SZ"
        :param date_str: "2021-10-15T06:44:58Z"
        """

        return time.mktime(datetime.datetime.strptime(date_str, fmt).timetuple())

    @classmethod
    def timestamp2string(cls, fmt: str, ts: int):
        """
        将时间戳转换为字符串
        :param fmt: "%m/%d/%Y, %H:%M:%S"
        :param ts: 1284101485
        :return: "2010-09-10 06:51:25"
        """
        ts = int(ts)
        return datetime.datetime.utcfromtimestamp(ts).strftime(fmt)

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        """
        校验密码
        :param plain_password: 明文密码
        :param hashed_password: hash后的密码
        :return:
        """
        return pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def gen_password_hash(cls, password):
        """
        生成密码hash2
        :param password:
        :return:
        """
        return pwd_context.hash(password)


class SingleInstance(type):
    """
    example:
        class single(metaclass=SingleInstance)
            def __init__(self):
                pass
            def say_hello(self, message="hello world"):
                print(message)
    """
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(SingleInstance, cls).__call__(*args, **kwargs)
        return cls._instance


class ApiJSONEncoder(json.JSONEncoder):
    """将ORM对象转换为字典"""

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        elif isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, set):
            return list(obj)
        elif isinstance(obj.__class__, DeclarativeMeta):
            data = {}
            fields = obj.__json__() if hasattr(obj, '__json__') else dir(obj)
            for field in [f for f in fields if not f.startswith('_')
                                               and f not in ['metadata', 'query', 'query_class']]:
                value = obj.__getattribute__(field)
                if callable(value):
                    continue
                try:
                    json.dumps(value)
                    data[field] = value
                except:
                    if isinstance(value, datetime.datetime):
                        data[field] = value.isoformat()
                    elif isinstance(value, datetime.date):
                        data[field] = value.isoformat()
                    elif isinstance(value, datetime.timedelta):
                        data[field] = (datetime.datetime.min + value).time().isoformat()
                    elif isinstance(value, decimal.Decimal):
                        data[field] = (str(value))
                    else:
                        data[field] = None
            return data

        return json.JSONEncoder.default(self, obj)


class ORM2JSONWrapped:
    """
    ORM对象转换为json装饰器
    example:
        @ORM2JSONWrapped
        def some_reader_db_api()
            return models.query()
    """
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            orm_obj = func(*args, **kwargs)
            json_data = json.dumps(orm_obj,
                                   cls=ApiJSONEncoder,
                                   ensure_ascii=False,
                                   separators=(',', ':'),
                                   )
            return json.loads(json_data)

        return wrapped_function


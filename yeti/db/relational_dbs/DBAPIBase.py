# !/usr/bin/env python3.9
# -*-coding:utf-8 -*-

"""
# Author   : Sunny
# @Time    : 2021/8/23 11:23 am
# @File    : db_api.py
# @Software: PyCharm
数据库的API操作，都在这个模块定义
"""
from oslo_db.sqlalchemy import enginefacade
from sqlalchemy import cast, Numeric, Float, desc, asc
from typing import List

from yeti.utils.utils import ORM2JSONWrapped
from yeti.exceptions import exceptions
from yeti.db.relational_dbs.ModelsBase import QueryClass

ASC = "asc"
DESC = "desc"


class DBCURDBase:
    """
    数据库基本操作类
    其他表要使用请直接继承
    example:
      from yeti.db.relational_dbs.DBAPIBase import DBCURDBase
      from .modules import User
      class User(DBAPIBase):
          module = User

      User.get_one()
    """
    in_transaction = False
    module = None
    max_page_size = 200

    @classmethod
    def insert_one(cls, data: dict, session=None, autocommit: bool = True):
        """
        插入一条数据
        :param data: 数据库k,v字典
        :param session: db session. 如果autocommit为False，则必须传入session
        :param autocommit: 是否自动提交，如果不自动提交，则需要手动commit
        :return:
        """
        if not session:
            session = cls.get_session()
        in_transaction = cls._is_session_in_transaction(session)
        result = session.add(cls.module(**data))
        if not in_transaction and autocommit:
            session.commit()
            session.close()
        return result

    @classmethod
    def insert_many(cls, rows: List[dict], session=None, autocommit: bool = True):
        """
        插入多条数据
        :param rows: 数据条目
        :param session: db session
        :param autocommit:
        :return:
        """
        if not session:
            session = cls.get_session()
        in_transaction = cls._is_session_in_transaction(session)
        for row in rows:
            session.add(cls.module(**row))

        if autocommit and not in_transaction:
            session.commit()
            session.close()

    @classmethod
    def delete_one(cls, _id, session=None, soft_delete: bool = True, autocommit: bool = True):
        """
        删除一条数据
        :param _id: 唯一索引
        :param session: db session
        :param soft_delete: 是否为软删除。True 将deleted字段置为1；False 将真实删除该数据
        :param autocommit:
        :return:
        """
        if not session:
            session = cls.get_session()
        in_transaction = cls._is_session_in_transaction(session)
        if soft_delete:
            session.query(cls.module).filter_by(**{"id": _id}).soft_delete()
        else:
            session.query(cls.module).filter_by(**{"id": _id}).delete()

        if autocommit and not in_transaction:
            session.commit()
            session.close()

    @classmethod
    def delete_many(cls, filters: dict, session=None, soft_delete: bool = True, autocommit: bool = True):
        """
        删除多条数据
        :param filters: 过滤条件
        :param session: db session
        :param soft_delete: 是否为软删除。True 将deleted字段置为1；False 将真实删除该数据
        :param autocommit:
        :return:
        """
        # pop the None value
        filters = cls._pop_none(filters)
        if not filters:
            raise exceptions.InternalError(msg_cn=f"filters 不能为空。 filters={filters}",
                                           msg_en=f"filters can not be None. filters={filters}"
                                           )
        if not session:
            session = cls.get_session()
        in_transaction = cls._is_session_in_transaction(session)
        if soft_delete:
            session.query(cls.module).filter_by(**filters).soft_delete()
        else:
            session.query(cls.module).filter_by(**filters).delete()
        if autocommit and not in_transaction:
            session.commit()
            session.close()

    @classmethod
    def update_one(cls, _id, value: dict, session=None, autocommit: bool = True):
        """
        更新一条数据
        :param _id: 唯一索引
        :param value: 需要更新的字段。其中，id字段不能被更新
        :param session: db session
        :param autocommit:
        :return:
        """
        value = cls._pop_none(value)
        value.pop("id", None)
        if not session:
            session = cls.get_session()
        in_transaction = cls._is_session_in_transaction(session)
        if value:
            session.query(cls.module).filter_by(**{"id": _id}).update(value)
        if autocommit and not in_transaction:
            session.commit()
            session.close()

    @classmethod
    def update_many(cls, filters: dict, value: dict, session=None, autocommit=True):
        """
        删除多条数据
        :param filters: 过滤条件
        :param session: db session
        :param value: 要更新的数据
        :param autocommit:
        :return:
        """
        # pop the None value
        filters = cls._pop_none(filters)
        if not filters:
            raise exceptions.InternalError(msg_cn=f"filters 不能为空。 filters={filters}",
                                           msg_en=f"filters can not be None. filters={filters}"
                                           )
        if not session:
            session = cls.get_session()
        in_transaction = cls._is_session_in_transaction(session)
        value = cls._pop_none(value)
        value.pop("id", None)
        if value:
            session.query(cls.module).filter_by(**filters).update(value)
        if autocommit and not in_transaction:
            session.commit()
            session.close()

    @classmethod
    @ORM2JSONWrapped()
    def get_one(cls, filters: dict, session=None, read_deleted=False, read_all=False):
        """
        获取一条数据, 默认返回deleted = 0的数据（未删除的数据）
        :param filters:
        :param session:
        :param read_deleted:
        :param read_all:
        :return:
        """
        if read_all is False:
            if read_deleted:
                filters["deleted"] = True
        else:
            filters["deleted"] = False
        if not session:
            session = cls.get_session()
        in_transaction = cls._is_session_in_transaction(session)
        result = session.query(cls.module).filter_by(**filters).first()
        if not in_transaction:
            session.close()
        return result

    @classmethod
    @ORM2JSONWrapped()
    def get_many(cls, filters: dict, session=None, read_deleted=False, read_all=False, start: int = 0,
                 length: int = 14, sort_by: str = "created_at", order: str = ASC):
        """
        获取多条数据
        :param filters: 过滤条件
        :param session: db session
        :param read_deleted:
        :param read_all:
        :param start: 起始页
        :param length: 页长度
        :param sort_by: 按数据库哪个健进行排序
        :param order: asc/desc 升序/降序
        :return:
        """
        if length > cls.max_page_size:
            raise exceptions.ParameterError(
                msg_en=f"page size maximum is {cls.max_page_size}",
                msg_cn=f"分页最大值不能超过 {cls.max_page_size}"
            )
        if read_all is False:
            if read_deleted:
                filters["deleted"] = True
        else:
            filters["deleted"] = False

        if not session:
            session = cls.get_session()
        in_transaction = cls._is_session_in_transaction(session)
        q = session.query(cls.module).filter_by(**filters)
        # sort
        q = cls._sort_result(q=q, order=order, sort_by=sort_by)
        # page
        q = cls._paging_result(q=q, start=start, length=length)
        result = {
            "count": q.count(),
            "data": q.all()
        }
        if not in_transaction:
            session.close()
        return result

    @classmethod
    def _paging_result(cls, q, start, length):
        """
        对数据进行分页
        :return:
        """
        if start and length:
            start = int(start)
            length = int(length)
            start = start * length - length
            q = q.limit(int(length)).offset(int(start))

        return q

    @classmethod
    def _sort_result(cls, q, order, sort_by):
        """
        排序
        :param q: the query object
        :param sort_by: order by column
        :param order: order method `asc/desc`
        :return:
        """
        order = order.lower()
        if order == ASC:
            sort_func = asc
        else:
            sort_func = desc
        query = q.order_by(sort_func(sort_by)
                           )
        return query

    @classmethod
    def get_session(cls):
        """
        获取数据库session
        在1.4版本中autocommit已被弃用. 2.0版本将不支持
        :return:
        """
        session_maker = enginefacade.writer.get_sessionmaker()
        session_maker.configure(**dict(autocommit=False,
                                       query_cls=QueryClass
                                       )
                                )
        session = session_maker()

        return session

    @classmethod
    def _pop_none(cls, filters: dict):
        """
        云除filters中value为None的数据
        :param filters:
        :return:
        """
        r = {}
        for k, v in filters.items():
            if v not in (None, ""):
                r[k] = v

        return r

    @classmethod
    def _is_session_in_transaction(cls, session):

        return session.in_transaction()

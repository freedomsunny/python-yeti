# !/usr/bin/env python3.9
# -*-coding:utf-8 -*-

"""
# Author   : Sunny
# @Time    : 2021/8/22 11:38 pm
# @File    : ModelsBase.py.py
# @Software: PyCharm
"""
import uuid
from oslo_db.sqlalchemy import models
from oslo_db.sqlalchemy.orm import Query
from sqlalchemy import Column
from sqlalchemy import orm
from sqlalchemy.ext import declarative
import sqlalchemy as sa
from oslo_utils import timeutils

from yeti.cfg.constants import (ID_FIELD_MAX_LENGTH,
                                )


class QueryClass(Query):
    def soft_delete(self, synchronize_session='evaluate'):
        entity = self.column_descriptions[0]['entity']
        return self.update({'deleted': True,
                            'updated_at': entity.updated_at,
                            'deleted_at': timeutils.utcnow()},
                           synchronize_session=synchronize_session
                           )


class _DBBase(models.ModelBase,
              models.TimestampMixin,
              models.SoftDeleteMixin
              ):
    """Base class for All Models."""

    __table_args__ = {'mysql_engine': 'InnoDB'}
    # init tables
    __table_initialized__ = False
    id = Column(sa.String(ID_FIELD_MAX_LENGTH),
                default=lambda: uuid.uuid4().hex,
                primary_key=True,
                unique=True,
                index=True,
                nullable=False
                )
    deleted = Column(sa.Boolean,
                     default=False
                     )

    @declarative.declared_attr
    def __tablename__(cls):
        # Use the pluralized name of the class as the table name.

        return cls.__name__.lower()

    def __iter__(self):
        self._i = iter(orm.object_mapper(self).columns)
        return self

    def next(self):
        n = next(self._i).name
        return n, getattr(self, n)

    __next__ = next

    def __repr__(self):
        """sqlalchemy based automatic __repr__ method."""
        items = ['%s=%r' % (col.name, getattr(self, col.name))
                 for col in self.__table__.columns]
        return "<%s.%s[object at %x] {%s}>" % (self.__class__.__module__,
                                               self.__class__.__name__,
                                               id(self), ', '.join(items))


BASE = declarative.declarative_base(cls=_DBBase)

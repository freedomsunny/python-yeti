# !/usr/bin/env python3.9
# -*-coding:utf-8 -*-

"""
# Author   : Sunny
# @Time    : 2021/9/15 5:22 pm
# @File    : dependencies.py
# @Software: PyCharm
"""
from typing import Optional, Any
from pydantic import BaseModel
from yeti.exceptions import constants as ec


class CommonQueryParams:
    """
    通用query参数
    # usage example
        from fastapi import Depends, FastAPI
        @app.get("/items/")
        async def read_items(commons: CommonQueryParams = Depends()):
            response = {}
            if commons.q:
                response.update({"q": commons.q})
            items = fake_items_db[commons.skip : commons.skip + commons.limit]
            response.update({"items": items})
            return response
    """

    def __init__(self, q: Optional[str] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


class CommonResponseModel(BaseModel):
    """
    通用响应模板
    example:
        class Item(BaseModel):
            name: str
            description: Optional[str] = None
            price: float
            tax: Optional[float] = None
            tags: List[str] = []

        @app.post("/items/", response_model=Item)
        async def create_item(item: Item):
            return item
    """
    business_code: Optional[int]
    msg_en: Optional[str] = ec.OK_EN_MESSAGE
    msg_cn: Optional["str"] = ec.OK_CN_MESSAGE
    data: Optional[Any]
    count: Optional[int]


def common_response(business_code: int = ec.OK_CODE,
                    msg_en: str = ec.OK_EN_MESSAGE,
                    msg_cn: str = ec.OK_CN_MESSAGE,
                    data: Any = None,
                    count: int = 0,
                    ):
    """
    用于响应客户端
    :param business_code:
    :param msg_en:
    :param msg_cn:
    :param data:
    :param count:
    :return:
    """

    return CommonResponseModel(**dict(business_code=business_code,
                                      msg_en=msg_en,
                                      msg_cn=msg_cn,
                                      data=data,
                                      count=count)
                               )

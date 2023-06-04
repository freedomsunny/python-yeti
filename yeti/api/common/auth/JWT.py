# !/usr/bin/env python3.9
# -*-coding:utf-8 -*-

"""
# Author   : Sunny
# @Time    : 2021/9/17 3:20 pm
# @File    : JWT.py
# @Software: PyCharm
Json Web Token Auth
see: https://jwt.io/
"""
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from yeti.api.common.data_scheme import JWTTokenResponse
from yeti.utils.utils import Utils
from yeti.cfg import CONF, constants
from yeti.exceptions import exceptions
from yeti.db.relational_dbs.db_api import UsersDBAPI

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/token")


class JWTAuth:
    """JWT认证类"""

    @classmethod
    def create_access_token(cls, data: dict, expires_delta: Optional[timedelta] = None):
        """
        生成jwt token
        :param data: 用户数据
        :param expires_delta: token有效时间
        :return:
        """
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=CONF.token_expire_minutes)
        data.update({"expire": str(expire)})
        token = jwt.encode(data, CONF.secret_key, algorithm=CONF.algorithm)
        return JWTTokenResponse(**dict(token=token)
                                )

    @classmethod
    async def get_current_user(cls, token: str = Depends(oauth2_scheme)):
        """验证当前用户token"""
        try:
            payload = jwt.decode(token, CONF.secret_key, algorithms=[CONF.algorithm])
            username: str = payload.get("username")
            if not username:
                return False
        except JWTError:
            raise exceptions.AuthError(msg_cn=f"无效token '{token}'",
                                       msg_en=f"invalid token '{token}'"
                                       )
        user = UsersDBAPI.get_one(filters=dict(username=username)
                                  )
        if not user:
            return False

        return user

    @classmethod
    def authenticate_user(cls, username: str, password: str):
        """验证用户"""
        user = UsersDBAPI.get_one(filters={"username": username})
        if not user:
            return False
        if not Utils.verify_password(password, user["password"]):
            return False
        return user

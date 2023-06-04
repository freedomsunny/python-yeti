# !/usr/bin/env python3.9
# -*-coding:utf-8 -*-

"""
# Author   : Sunny
# @Time    : 2021/11/17 9:50 pm
# @File    : auth.py
# @Software: PyCharm
"""
from fastapi import APIRouter

from yeti.api.common.data_scheme import JWTTokenResponse, JWTPasswordAuth
from yeti.api.common.auth import JWTAuth
from yeti.exceptions import exceptions

router = APIRouter(tags=["example"],
                   )


@router.post("/v1/token", response_model=JWTTokenResponse)
async def jwt_access_token(body_data: JWTPasswordAuth):
    user = JWTAuth.authenticate_user(body_data.username, body_data.password)
    if not user:
        raise exceptions.AuthError(msg_en="Incorrect username or password",
                                   msg_cn="无效的用户名或密码")
    access_token = JWTAuth.create_access_token(
        data=user
    )
    return access_token

# !/usr/bin/env python3.9
# -*-coding:utf-8 -*-

"""
# Author   : Sunny
# @Time    : 2021/9/15 10:48 pm
# @File    : middlewares.py
# @Software: PyCharm

访问接口时先进行处理的函数
优先级：
后定义的函数先执行
"""
import traceback
from json.decoder import JSONDecodeError
from fastapi import status, Request, Response
from starlette.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp, Scope, Receive, Send
from starlette.responses import JSONResponse
from starlette.datastructures import URL, Headers
from starlette.requests import ClientDisconnect

from yeti.api.common.data_scheme import (
    HttpLoggingRequestContext,
    HttpLoggingResponseContext,
    WebsocketResponseContext,
    WebsocketRequestContext
)
from yeti.api.common import get_app
from yeti.log.logger import LOG
from yeti.exceptions import constants, exceptions
from yeti.api.common.dependencies import CommonResponseModel
from yeti.api.common.g import init_g
from yeti.api.common.auth import JWTAuth
from yeti.cfg import CONF

app = get_app()


async def logging_request(request: Request):
    """
    why use tow different method for logging request and response? see below:
    https://github.com/tiangolo/fastapi/issues/394
    :return:
    """
    # logging incoming request
    try:
        json_body = await request.json()
        # may be not json
    except (UnicodeDecodeError, JSONDecodeError):
        json_body = b""
    request_context = dict(
        client_ip=str(request.client),
        requests_url=str(request.url),
        request_headers=request.headers,
        request_method=request.method,
        request_body=json_body
    )
    LOG.info("Incoming request: {}".format(HttpLoggingRequestContext(**request_context).dict())
             )


async def jwt_token_auth(request: Request):
    """JWT认证，验证token是否合法有效
    token可携带的位置：
      1. url: token=$token
      2. header: authorization: Bearer $token
    """
    token = None
    if request.url.path not in CONF.exclude_auth_path:
        if request.headers.get("authorization"):
            token = request.headers.get("authorization").split()[-1]
        else:
            token = request.query_params.get("token")
    if not token:
        raise exceptions.AuthError(msg_en="token is required",
                                   msg_cn="未提供token")

    await JWTAuth.get_current_user(token=token)


class CommonMiddleware:
    """
    通用中间件，请求前、请求后的一些逻辑处理。这里主要用于记录日志
    """

    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        """
        通用中间件
        1.记录http错误日志，并返回JSON数据
        2.记录Websocket连接日志
        ASGI规范: https://asgi.readthedocs.io/en/latest/index.html
        :param scope:
        :param receive:
        :param send:
        :return:
        """
        # init the global var peer request
        init_g()
        # where the request is websocket
        if scope["type"] == "websocket":
            req_info = dict(
                request_type=str(scope["type"]),
                client_ip_address=str(scope["client"]),
                requests_url=str(URL(scope=scope)),
                request_headers=dict(Headers(scope=scope))
            )
            user_context = WebsocketRequestContext(**req_info)
            try:
                # logging
                LOG.info("Websocket new connect: {}".format(user_context.dict())
                         )
                await self.app(scope, receive, send)
                LOG.info("connected success")
            # client has disconnected
            except ClientDisconnect:
                LOG.info(f"client {user_context.client_ip_address} has disconnected")
            except Exception as e:
                LOG.error(traceback.format_exc())
                print(e)
        else:
            try:
                await self.app(scope, receive, send)
            except Exception as e:
                info = dict(business_code=getattr(e, "business_code", constants.UNKNOWN_EXCEPTION_CODE),
                            http_code=getattr(e, "http_code", status.HTTP_500_INTERNAL_SERVER_ERROR),
                            msg_en=getattr(e, "msg_en", constants.DEFAULT_UNKNOWN_EN_MSG),
                            msg_cn=getattr(e, "msg_cn", constants.DEFAULT_UNKNOWN_CN_MSG),
                            details=f"{e}"
                            )
                if any(hasattr(e, attr) for attr in ["business_code", "http_code", "msg_en", "msg_cn"]):
                    LOG.error(f"{info['http_code']} {info['details']}")
                else:
                    LOG.error(traceback.format_exc())
                # about response. see: https://www.starlette.io/responses/
                response = JSONResponse(content=CommonResponseModel(**info).dict(),
                                        status_code=info["http_code"]
                                        )
                await response(scope, receive, send)


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# logging
app.add_middleware(CommonMiddleware)

# 返回前需要执行的函数
# 顺序: 列表越靠前越优先执行
before_request_middlewares = [
    logging_request,
    jwt_token_auth

]

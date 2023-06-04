# !/usr/bin/env python3.9
# -*-coding:utf-8 -*-

"""
# Author   : Sunny
# @Time    : 2021/8/3 23:48 pm
# @File    : HttpHelper.py
# @Software: PyCharm
"""
import copy
from typing import Awaitable
from urllib import parse
import operator
import aiohttp
from socket import AF_INET
from typing import Optional, Any
from pydantic import BaseModel
from aiohttp.client_exceptions import ContentTypeError

from .retry import AsyncioRetry
from yeti.exceptions import exceptions, constants
from yeti.log.logger import LOG
from yeti.api.common import get_app

# Don't create a session per request
# a session per application or site(e.g: one for Github and other one for Facebook)
# see: https://docs.aiohttp.org/en/stable/client_quickstart.html
aio_http_session = None
app = get_app()


class AsyncHttpRequestModel(BaseModel):
    url: Optional[str]
    headers: Optional[dict]
    method: Optional[str]
    body: Optional[Any] = None
    cookies: Optional[dict]
    context: Optional[Any]


class AsyncHttpResponseModel(BaseModel):
    code: Optional[int] = constants.OK_CODE
    headers: Optional[dict]
    body: Optional[Any] = None
    text: Optional[str]
    error_msg: Optional[str]


def get_aiohttp_session(cookies=None, time_out=100, connect=None) -> aiohttp.ClientSession:
    """
    初始化http session
    about time out: https://docs.aiohttp.org/en/stable/client_quickstart.html#timeouts

    :return:
    """
    global aio_http_session
    timeout = aiohttp.ClientTimeout(total=time_out, connect=connect)
    connector = aiohttp.TCPConnector(family=AF_INET)
    # if passed cookies, return a new session object
    if cookies:
        return aiohttp.ClientSession(timeout=timeout, connector=connector, cookies=cookies)
    elif aio_http_session is None:
        aio_http_session = aiohttp.ClientSession(timeout=timeout, connector=connector)

    return aio_http_session


@app.on_event("shutdown")
async def close_aiohttp_session() -> None:
    global aio_http_session
    if aio_http_session:
        await aio_http_session.close()
        aio_http_session = None


def http_sender(url: str,
                method: str,
                query_params: dict = None,
                body: dict = None,
                headers: dict = None,
                cookies: dict = None,
                context: Any = None,
                time_out: int = 5,
                retry_times: int = 3,
                delay: int = 1,
                logger: callable = LOG
                ) -> Awaitable:
    method = method.lower()
    """
    more about aiohttp client. see: https://docs.aiohttp.org/en/stable/client_quickstart.html
    """

    @AsyncioRetry(retry_times=retry_times, delay=delay, logger=logger)
    async def http_sender_inner() -> Awaitable:
        response_model = AsyncHttpResponseModel()
        getter = operator.attrgetter(method)
        session = get_aiohttp_session(cookies=cookies, time_out=time_out)
        if query_params:
            for k, v in copy.deepcopy(query_params).items():
                if v in ("", None):
                    query_params.pop(k, None)
        request_model = AsyncHttpRequestModel(
            **{"url": ("%s?%s" % (url, parse.urlencode(query_params)) if query_params else url),
               "method": method,
               "body": body,
               "headers": headers,
               "cookies": cookies,
               "context": context
               })
        LOG.info("sending request: {}".format(request_model.dict())
                 )
        m = getter(session)
        async with m(url, params=query_params, json=body, headers=headers) as response:
            try:
                response_model.body = await response.json()
            # maybe the response not json data
            except ContentTypeError:
                response_model.text = await response.text()
            response_model.code = response.status
            response_model.headers = response.headers

            # finally logging & close session if true
            if cookies:
                await session.close()
                # error happened
            if response_model.code >= 400:
                LOG.error("response: {}".format(response_model.dict())
                          )
                # for retry
                # raise exceptions.SendRequestError
            else:
                LOG.info("response: {}".format(response_model.dict())
                         )

            return response

    return http_sender_inner()

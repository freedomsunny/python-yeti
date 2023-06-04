# !/usr/bin/env python3.9
# -*-coding:utf-8 -*-

"""
# Author   : Sunny
# @Time    : 2021/10/9 10:22 am
# @File    : g.py
# @Software: PyCharm
"""

import contextvars
import types

request_global = contextvars.ContextVar("request_global",
                                        default=types.SimpleNamespace()
                                        )


# This is the only public API
def g():
    """
    global var store&get per request
    ref: https://gist.github.com/glenfant/2fe530e5a2b90c28608165b5a18afcaf
    usage example:
    asgi.py
        # init var
        @app.middleware("http")
        async def init_requestvars(request: fastapi.Request, call_next):
            # Customize that SimpleNamespace with hatever you need
            client_info = request.client
            initial_g = types.SimpleNamespace()
            requestvars.request_global.set(initial_g)
            # requestvars.request_global.set(client_info)
            response = await call_next(request)
            g().user_info = {"name": "test", "age": 10}
            return response

    handler.py
        # import g
        from g import g
        router = fastapi.APIRouter()


        @router.get("/foo")
        async def foo_route(q: str = ""):
            # set var
            g().blah = q
            # get var
            print(g().blah)
            print(g().user_info)
            return {"result": ""}

        :return:
    """

    return request_global.get()


def init_g():
    """初始化全局变量"""
    initial_g = types.SimpleNamespace()
    request_global.set(initial_g)

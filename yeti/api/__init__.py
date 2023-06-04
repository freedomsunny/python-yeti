# !/usr/bin/env python3.9
# -*-coding:utf-8 -*-

"""
# Author   : Sunny
# @Time    : 2021/8/3 5:03 pm
# @File    : __init__.py.py
# @Software: PyCharm
"""
import os
from fastapi import Depends
from importlib.machinery import SourceFileLoader

import yeti
from yeti.cfg import CONF
from yeti.log.logger import LOG
from yeti.api.common import get_app, middlewares

app = get_app()
load_info = set()


def automatic_load_endpoints():
    """
    自动加载API
    :return:
    """
    for load_dir in set(CONF.api_load_dirs):
        load_dir = load_dir.replace(".", "/")
        # api所在根目录
        handlers_root_path = f"{os.path.dirname(yeti.__file__)}/{load_dir}"
        handler_files = os.walk(handlers_root_path)
        for i in handler_files:
            dir_path, dir_names, file_names = i
            for f in file_names:
                if f.endswith(".py") and f not in ("__init__.py", ):
                    module_name = f.replace(".py", "")
                    module_path = f"{dir_path}/{f}"
                    module = SourceFileLoader(module_name, module_path).load_module()
                    try:
                        if module not in load_info:
                            dependencies = []
                            # load the middlewares
                            for fn in middlewares.before_request_middlewares:
                                if not callable(fn):
                                    LOG.warning(f"middleware {fn} is not callable")
                                else:
                                    dependencies.append(Depends(fn))

                        app.include_router(module.router, dependencies=dependencies)
                        load_info.add(module)
                        LOG.success(f"Load api {module} Success")
                    except Exception as e:
                        LOG.warning(f"Load api module '{dir_path}/{f}' error. {e}")


@app.on_event("startup")
def main():
    automatic_load_endpoints()

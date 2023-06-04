# !/usr/bin/env python3.9
# -*-coding:utf-8 -*-

"""
# Author   : Sunny
# @Time    : 2021/8/8 10:09 pm
# @File    : yetid.py
# @Software: PyCharm
# description: start app script
"""
import uvicorn
from yeti.cfg import CONF


def main():
    # run server
    uvicorn.run("yeti.api:app",
                host=CONF.listen,
                port=CONF.port,
                workers=CONF.process_count
                )


if __name__ == "__main__":
    main()

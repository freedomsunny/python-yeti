# !/usr/bin/env python3.9
# -*-coding:utf-8 -*-

"""
# Author   : Sunny
# @Time    : 2021/8/3 5:25 pm
# @File    : setup.py
# @Software: PyCharm
"""
from setuptools import setup

setup(
    name='yourscript',
    version='0.1.0',
    py_modules=['yourscript'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'yourscript = yourscript:cli',
        ],
    },
)

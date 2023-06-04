# !/usr/bin/env python3.9
# -*-coding:utf-8 -*-

"""
# Author   : Sunny
# @Time    : 2021/11/30 9:39 pm
# @File    : user_manager.py
# @Software: PyCharm
"""
import click

from yeti.db.relational_dbs.db_api import UsersDBAPI
from yeti.utils.utils import Utils
from yeti.log.logger import LOG
from yeti.exceptions import exceptions


@click.command(context_settings=dict(ignore_unknown_options=True,
                                     allow_extra_args=True
                                     ))
@click.option('--username', required=True,
              help='The username')
@click.option('--password', required=True,
              help='The password')
@click.option('--status', default=1,
              help='The user status')
def user_manager(username, password, status):
    try:
        r = UsersDBAPI.get_one({"username": username.strip()})
        if r:
            raise exceptions.ParameterError(msg_cn=f"用户: [{username}] 已存在",
                                            msg_en=f"user: [{username}] already exists"
                                            )
        hashed_password = Utils.gen_password_hash(password=password)
        UsersDBAPI.insert_one(data={"username": username,
                                    "password": hashed_password,
                                    "status": status}
                              )
        LOG.success(f"add user [{username}] from cli")
    except:
        LOG.exception(f"Add user [{username}] fail from cli")


if __name__ == "__main__":
    user_manager()

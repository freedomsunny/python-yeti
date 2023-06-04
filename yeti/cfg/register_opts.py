# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : register_opts.py
# Time       ：27/05/2021 17:29
# Author     ：Sunny
# version    ：python 3.7
# Description：
ref: https://docs.openstack.org/oslo.config/latest/reference/index.html
配置项优先级：
1.Command Line
2.Environment Variables
3.Config Files from --config-dir（多个文件时，文件后面会覆盖前面的配置）
4.Config Files from Internal（程序内部配置项）

配置项支持从以下位置导入：
1.本地文件
2.远程文件(HTTP)
"""
import re
import os
import sys
from oslo_config import cfg
from oslo_config import types

from yeti.utils.utils import SingleInstance

DEFAULT_OPT_SECTION = "DEFAULT"

types_mapping = {
    # boolean
    bool: types.Boolean,
    # 浮点数
    float: types.Float,
    # 整数
    int: types.Integer,
    # dict类型
    dict: types.Dict,
    # list
    list: types.List,
    # 普通字符串
    str: types.String
}


class RegisterOptions(metaclass=SingleInstance):
    _DEFAULT_OPT_TYPE = str

    def __init__(self):
        cfg.ConfigOpts()

    @classmethod
    def register_cli_opts(cls, conf, opts, group=None):
        """
        register options to command line
        all options registered [DEFAULT] section. not accept other section
        :return:
        """
        conf.register_cli_opts(opts)

    @classmethod
    def register_group(cls, group):
        """
        注册组
        :param group:
        :return:
        """
        # Define an option group
        grp = cfg.OptGroup(group)
        # Register your config group
        return cfg.CONF.register_group(grp)

    @classmethod
    def register_opts(cls, opts, conf):
        """
        所有配置项默认配置在[DEFAULT]分组中
        Note: 如果没有指定配置项的类型，默认为String类型
        :return:
        """
        register_opts = []
        for s in opts:
            name = s["name"]
            _type = s["type"]
            default = s.get("default", "")
            _help = s.get("help", "")
            if name == "config_file":
                # cli is high priority
                if "--config-file=" in "".join(sys.argv):
                    config_file = cls.get_config_file_from_argv(sys.argv)
                # if cli not pass. use default
                else:
                    config_file = f"--config-file={default}"
                # check the file is it exist
                # if not. raise exceptions
                conf_file_path = config_file.split("=")[1]
                if not os.path.isfile(conf_file_path):
                    raise OSError(f"No such file or directory: '{conf_file_path}'")
                cfg.CONF([config_file])
            else:
                _type = types_mapping[_type]()
                register_opts.append(cfg.Opt(name=name,
                                             type=_type,
                                             default=default,
                                             help=_help
                                             )
                                     )
        # register those opts
        conf.register_opts(register_opts)
        # finally register cli/config file
        # conf.register_cli_opts(register_opts)
        # sort argv list
        # argv = cls.sort_argv(sys.argv)
        # conf(argv[1:])

        return conf

    @classmethod
    def sort_argv(cls, argv):
        """
        --config-file 必须在位于第一个参数
        ['yetid.py', '--port=9999', '--config-file=/etc/yeti/config.ini'] -->
        ['yetid.py', '--config-file=/etc/yeti/config.ini', '--port=9999']
        :param argv:
        :return:
        """
        result = []
        for index, element in enumerate(argv):
            if "config-file" in element:
                result.insert(1, element)
            else:
                result.append(element)

        return result

    @classmethod
    def get_config_file_from_argv(cls, argv: list):
        """
        从命令行中获取配置文件
        :return:
        """
        argv_str = " ".join(argv)
        pat = re.compile(r".+? (--config-file=.+?) .+?")
        r = re.match(pat, argv_str)
        if r:
            return r.group(1)
        return None


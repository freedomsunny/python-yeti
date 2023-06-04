#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
# @Time    : 2021/6/24 4:05 pm
# @Author  : Sunny
# @Site    : 
# @File    : options.py
# @Software: PyCharm
import os

# you can define your owner options at below
user_opts = [
    {
        "name": "configA",
        "type": str,
        "default": "configA------",
        "help": "configA-",
        "kw_args": {}
    },
]


# project internal opts
_project_internal_opts = [
    {
        "name": "config_file",
        "type": str,
        "default": "/etc/yeti/config.ini",
        "help": "the config file",
        "kw_args": {}
    },
    {
        "name": "listen",
        "type": str,
        "default": "127.0.0.1",
        "help": "the app bind address. default: 127.0.0.1",
        "kw_args": {}
    },
    {
        "name": "port",
        "type": int,
        "default": 8080,
        "help": "listen port default: 8080",
        "kw_args": {
            "min": 1,
            "max": 65535
        }
    },
    {
        "name": "process_count",
        "type": int,
        "default": os.cpu_count(),
        "help": f"number of process. default is cpu count: {os.cpu_count()}",
        "kw_args": {}
    },
    {
        "name": "logging_level",
        "type": str,
        "default": "INFO",
        "help": "the logging level, accept one of the: (TRACE DEBUG INFO SUCCESS WARNING ERROR CRITICAL)",
        "kw_args": {}
    },
    {
        "name": "api_load_dirs",
        "type": list,
        "default": ["api.handlers",
                    ],
        "help": "those dir will be automatic loading to endpoint",
        "kw_args": {}
    },
    {
        "name": "logging_path",
        "type": str,
        "default": "/var/log/yeti/yeti.log",
        "help": "the logging file",
        "kw_args": {}
    },
    {
        "name": "logging_rotation",
        "type": str,
        "default": "1 GB",
        "help": "A condition indicating whenever the current logged file should be closed and a new one started",
        "kw_args": {}
    },
    {
        "name": "logging_retention",
        "type": str,
        "default": "",
        "help": "A directive filtering old files that should be removed during rotation or end of program.",
        "kw_args": {}
    },
    {
        "name": "logging_format",
        "type": str,
        "default": "{time:YYYY-MM-DD HH:mm:ss.SSS} {process} {level} {name}.{file}.{function}():{line} {message}",
        "help": "The logger format. ref: https://loguru.readthedocs.io/en/stable/api/logger.html",
        "kw_args": {}
    },
    {
        "name": "sql_connection",
        "type": str,
        # "default": "sqlite+pysqlite:///:memory:",
        "default": "mysql+pymysql://root:Ebi8WQXX67fVFhYc@127.0.0.1/default_db?charset=utf8mb4",
        "help": "The sql connection string",
        "kw_args": {}
    },
    {
        "name": "connection_poll_size",
        "type": int,
        "default": 20,
        "help": "The sql connection pool size",
        "kw_args": {}
    },
    {
        "name": "cached_backend",
        "type": str,
        "default": "redis://127.0.0.1:6379/0",
        "help": "cache connect uri",
        "kw_args": {}
    },
    {
        "name": "upload_file_path",
        "type": str,
        "default": "/data",
        "help": "the upload data dir",
        "kw_args": {}
    },
    {
        "name": "enable_websocket",
        "type": bool,
        "default": True,
        "help": "is enable websocket",
        "kw_args": {}
    },
    {
        "name": "websocket_topic",
        "type": str,
        "default": "ws_topic",
        "help": "websocket pub/sub channel name",
        "kw_args": {}
    },
    # Authentication
    {
        "name": "auth_type",
        "type": str,
        "default": "JWT",
        "help": "the auth.md type, accept [jwt]",
        "kw_args": {}
    },
    {
        "name": "secret_key",
        "type": str,
        "default": "",
        "help": "the token hashing secret key. you can use command `openssl rand -hex 32` to generate",
        "kw_args": {}
    },
    {
        "name": "token_expire_minutes",
        "type": int,
        "default": 30,
        "help": "The token expire time (in minutes)",
        "kw_args": {}
    },
    {
        "name": "algorithm",
        "type": str,
        "default": "HS256",
        "help": "The hashing algorithm. default is HS256",
        "kw_args": {}
    },
    {
        "name": "exclude_auth_path",
        "type": list,
        "default": [],
        "help": "exclude auth.md path",
        "kw_args": {}
    },
]


conf_opts = _project_internal_opts + user_opts

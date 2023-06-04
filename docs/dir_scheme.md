# 项目结构说明

```python
├── bin    //存放可执行文件。如启动项目的yetid.py
├── cli    // 项目的命令行工具脚本
├── docs   //项目文档目录
├── etc    //配置文件示例
└── yeti
    ├── api   //存放与API相关的目录
    │   ├── common  //存放API通用库的目录
    │   │   ├── auth   //与认证相关的库
    │   │   ├── data_scheme //接口请求&返回数据结构定义
    │   ├── handlers      // 接口在这个目录定义
    │   │   ├── v1   //版本1
    │   │   └── ws   //WebSocket
    ├── cache    //缓存，当前版本仅支持redis，未来将支持memcached
    ├── cfg      //注册配置、定义配置
    ├── db       //数据库
    │   ├── nosql_dbs    //非关系型数据库（当前版本不支持）
    │   │   ├── es //不支持
    │   │   └── mongodb //不支持
    │   └── relational_dbs //关系型数据库
    │       ├── models    //表结构
    ├── exceptions    //异常定义
    ├── jobs    //周期/定时/异步任务(暂不支持)
    ├── libs    //在这里写你的业务逻辑
    ├── log     //日志
    ├── tests   //单元测试(暂不支持，可以自己写)
    └── utils   //常用工具
```
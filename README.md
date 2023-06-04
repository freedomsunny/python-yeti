# 异步web开发框架(YETI)
##### 本框架主要面向业务快速开发，开箱即用。学习成本低，适合新手学习，老手直接用于项目开发
# 功能
1. Async(based on [uvicorn](https://www.uvicorn.org/))
2. Cache(based on [pyredis](https://github.com/andymccurdy/redis-py) and [aioredis](https://aioredis.readthedocs.io/en/latest/getting-started/) include redis memcached)
3. DB(based on [sqlalchemy](https://docs.sqlalchemy.org/en/14/). include mysql mongodb)
4. Distributed Jobs(based on [celery](https://docs.celeryproject.org/en/stable/getting-started/introduction.html) )
5. logging(based on [loguru](https://github.com/Delgan/loguru))
6. config(based on [oslo.config(OpenStackPorject)](https://github.com/openstack/oslo.config))
7. Auth([JWT](https://jwt.io/))
8. CLI(based on [click](https://click.palletsprojects.com/en/8.0.x/))
9. websocket(based on [fastapi](https://fastapi.tiangolo.com/))
10. exception handler
11. async http client automatic manager connection pool(based on [aiohttp](https://docs.aiohttp.org/en/latest/client_quickstart.html))

# 环境依赖
#### python3.7+
#### redis server
#### mysql 5.7+ OR Mariadb 10.0+

# Quick Start
## 方式一：手动启动项目
### step1: 下载项目
```angular2html
git clone https://gitee.com/hyjsunny/yeti.git
```
### step2: 设置环境变量
```angular2html
export PROJECTNAME=yeti
# cd $PROJECTNAME/
# export PYTHONPATH=$PYTHONPATH:`pwd`
```
### step3: 安装依赖
```angular2html
# pip3 install -r requirements.txt
```
### step4: 修改配置
````angular2html
# mkdir -p /etc/$PROJECTNAME/
# cp etc/config.ini.simple /etc/$PROJECTNAME/config.ini

修改配置文件中的数据库连、Redis连接串
sql_connection = "your db connection string"
cached_backend = "your redis connection string"
````
### step5: 启动项目
默认监听在127.0.0.1:8000
```angular2html
# python3 bin/yetid.py
```
or<br>

指定配置文件
```
python3 bin/yetid.py --config-file=/path/your/config.ini
```
## 方式二：Docker方式启动项目(推荐)
### step1: 安装Docker
根据自己的操作系统选择合适的安装方式。参考: [Docker安装](https://docs.docker.com/engine/install/)
### step2: 启动环境依赖容器
```angular2html
# 启动redis
docker run --net host \
--name redis-server \
-d redis

# 启动mariadb
docker run --name mariadb \
--net host \
-e MYSQL_ROOT_PASSWORD=Ebi8WQXX67fVFhYc \
-e MARIADB_DATABASE=default_db \
-d mariadb
```

### step3: 下载项目
```angular2html
git clone https://gitee.com/hyjsunny/yeti.git
# 设置项目名
export PROJECTNAME=yeti
```
### step4: 修改配置文件
```angular2html
mkdir -p /etc/$PROJECTNAME
cp $PROJECTNAME/etc/config.ini.simple /etc/$PROJECTNAME/config.ini
vim /etc/$PROJECTNAME/config.ini

sql_connection = "your sql connection string"
cached_backend = "your redis connection string"
listen = "listen address"
port = "listen port"
```

### step5: 构建并启动容器
```angular2html
\cp $PROJECTNAME/Dockerfile . && \
docker build --build-arg PROJECTNAME=$PROJECTNAME --build-arg TZ=Asia/Shanghai -t $PROJECTNAME:latest . && \
docker run --name $PROJECTNAME --net host -v /etc/$PROJECTNAME/:/etc/$PROJECTNAME/ -v /var/log/:/var/log/ -d $PROJECTNAME
```

**重要提示** <br>
以上仅作为测试使用，生产环境请谨慎使用

## 测试
```python
# curl http://127.0.0.1:8080/helloword
{"result": "hello word"}
```

# 目录结构说明
### [项目目录结构说明](docs/dir_scheme.md#项目结构说明)    

# 接口开发
### [接口开发](docs/api.md#接口开发说明)   

# Websocket
### [websocket](docs/websocket.md#websocket)

# 日志
### [日志](docs/logging.md#日志)

# 配置
### [配置](docs/config.md#配置)

# 数据库
### [数据库](docs/database.md#数据库)

# 缓存
### [缓存](docs/cache.md#缓存)

# 异步HTTP客户端
### [aiohttp客户端](docs/aiohttp.md#异步http客户端工具)

# 定时/异步任务
暂定celery，目前还没有集成

# 认证
### [认证](docs/auth.md#认证)

# 命令行
### [命令行](docs/cli.md#命令行脚本)

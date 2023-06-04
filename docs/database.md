# 数据库
基于sqlalchemy 数据库目前支持关系型数据库：PGSQL、Mysql、Mariadb

## 定义模型
模型定义在yeti/db/relational_dbs/models/models.py
```python
import sqlalchemy as sa
from yeti.db.relational_dbs import ModelsBase


class Users(ModelsBase.BASE):

    username = sa.Column(sa.String(64))
    password = sa.Column(sa.String(64), default="your password")


init_tables_list = [
    Users
]

注意要点：
1. 在init_tables_list中的表将会自动创建表结构
2. 表名默认小写类名，如果要自定义表名。请增加类属性 __tablename__ = "your table name"
```

## 定义数据库API
数据库API需引用DBCURDBase类，该类包含了基础的增、删、改查方法
```python
# file db_api.py
from yeti.db.relational_dbs.models.models import Users
from yeti.db.relational_dbs.DBAPIBase import DBCURDBase


class UsersDBAPI(DBCURDBase):
    """user表"""
    module = Users

    @classmethod
    def some_extent_db_api(cls):
        """扩展的API"""
        pass
```

### 使用数据库API
```python
# 引用定义的数据表module
from yeti.db.relational_dbs.db_api import UsersDBAPI



def transaction_example():
    """事务示例"""
    # 先获取一个session
    session = UsersDBAPI.get_session()
    # 开启事务
    with session.begin():
        # 没有异常会自动commit事务
        # 发生异常会自动rollback事务
        UsersDBAPI.insert_one(session=session,
                              data={"username": "test111", "password": "password", "status": 1},
                      )

def none_transaction_example():
    """非事务数据库操作"""

    UsersDBAPI.insert_many(rows=[{"username": "test1", "password": "password1", "status": 1},
                                 {"username": "test2", "password": "password2", "status": 1},
                                 {"username": "test3", "password": "password3", "status": 1},
                                 {"username": "test4", "password": "password4", "status": 1}]
                           )

```
### DBCURDBase类方法
|方法名|说明|
| :-----| :---- |
|insert_one|用于插入一条数据|
|insert_many|用于插入多条数据|
|delete_one|用于删除一条数据|
|delete_many|用于删除多条数据|
|update_one|用于更新一条数据|
|update_many|用于更新多条数据|
|get_one|用于获取一条数据|
|get_many|用于获取多条数据（默认升序排序，黑夜分页14条数据）|
|get_session|用于获取一个会话（开启事务时）|

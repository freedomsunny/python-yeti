# 配置

# 定义配置
1. 编辑cfg/options.py，1个配置项=1个字典元素，按如下结构进行配置：
```
    {
        "name": "process_count",    //配置的名称 
        "type": int,                //配置的数据类型
        "default": os.cpu_count(),  //默认值
        "help": f"number of process. default is cpu count: {os.cpu_count()}", //帮助信息
        "kw_args": {}               //参数，如：int类型有max=100, min=10（详见官方文档）
    }
```
2. 配置文件（默认/etc/yeti/config.ini， 在命令行中--config-file=/etc/path/yourconfig.ini覆盖）
```
# vim /etc/yeti/config.ini
[DEFAULT]
....
process_count = 8    //与第一步配置的名称、类型必须相同
....
```
3. 使用配置
```python
from yeti.cfg import CONF
CONF.process_count
```

## 配置优先级(从高到低)
1. 程序默认配置文件(/etc/yeti/conf.ini)
2. 通过命令行--config-file=path_to_conf.ini指定的配置文件
3. 程序内部options.py定义的配置项
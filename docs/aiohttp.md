# 异步http客户端工具
基于aiohttp，用于处理所有的http请求请使用该库。具有自动管理http连接池、异常重试、请求&返回日志记录的功能

## 使用方法
```python
from yeti.utils.HttpHelper import http_sender

response = await http_sender(url="http://127.0.0.1/v1/users",
                             method="POST",
                             body={"name": "sunny"}
                             )

print(resp.json())
print(resp.text())
print(resp.status())
print(resp.headers)
```
# websocket
本框架Websocket利用redis订阅&发布功能，解决了多进程、多节点间通信问题。架构简单支持并发量高
## 代码示例
对应文件：yeti.api.handlers.ws.ws.py
```python
from typing import Any
from fastapi import WebSocket, WebSocketDisconnect
from fastapi import APIRouter

from yeti.api import get_app
from yeti.api.handlers.ws import ws_connector

app = get_app()
router = APIRouter(tags=["websocket"],
                   )


# if CONF.enable_websocket is True:
@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: Any):
    # Accept new client connect
    await ws_connector.connect(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            if message:
                # 广播消息，每个节点&进程都会收到
                await ws_connector.send_message(message=message)
    except WebSocketDisconnect:
        # 用户离开消息，每个节点&进程都会收到
        await ws_connector.disconnect(websocket, "{} has disconnect".format(client_id)
                                      )
```
## 配置项
```python
# 是否开启websocket功能
enable_websocket = off
# 订阅的频道，在此频道内的所有进程/节点都会收到订阅消息
websocket_topic = ws_topic
# 消息管道，目前仅支付redis
channel_driver = redis
```
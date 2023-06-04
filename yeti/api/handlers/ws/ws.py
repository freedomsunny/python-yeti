# !/usr/bin/env python3.9
# -*-coding:utf-8 -*-

"""
# Author   : Sunny
# @Time    : 2021/9/18 9:59 am
# @File    : ws.py
# @Software: PyCharm
"""
from typing import Any
from fastapi import WebSocket, WebSocketDisconnect
from fastapi import APIRouter

from yeti.api import get_app
from yeti.api.handlers.ws import ws_connector
from yeti.exceptions import exceptions
from yeti.cfg import CONF

app = get_app()
router = APIRouter(tags=["websocket"],
                   )


if CONF.enable_websocket:
    @router.websocket("/ws/{client_id}")
    async def websocket_endpoint(websocket: WebSocket, client_id: Any):
        # Accept new client connect
        await ws_connector.connect(websocket)
        try:
            while True:
                message = await websocket.receive_text()
                if message:
                    await ws_connector.send_message(message=message)
        except WebSocketDisconnect:
            # user disconnect
            await ws_connector.disconnect(websocket, "{} has disconnect".format(client_id)
                                          )

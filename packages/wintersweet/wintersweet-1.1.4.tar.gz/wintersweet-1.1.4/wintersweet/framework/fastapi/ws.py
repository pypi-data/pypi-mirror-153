

import asyncio
import traceback

from typing import Dict
from starlette.websockets import WebSocket, WebSocketDisconnect, WebSocketState

from wintersweet.utils.base import Utils


class WsChatConnectionManager:
    """ws会话管理器，超时无回应自动断开
    Example：
    >>>manager = WsChatConnectionManager()
    >>>router = APIRouter()

    >>>@router.websocket("/ws/{user_id}")
    >>>async def websocket_endpoint(ws: WebSocket, user_id: int=Query(...)):
    >>>     await manager.append(user_id, ws, MessageHandler)
    >>>     await manager.handle_message(user_id)
    """
    def __init__(self, limit=None, heartbeat_timeout=10, timeout_count=3):
        self._limit = limit
        self._heartbeat_timeout = heartbeat_timeout
        self._connections: Dict[str, WebSocket] = {}
        self._message_handlers = {}
        self._timeout_count = timeout_count
        self._lock = asyncio.Lock()

    async def append(self, key, ws, message_handle_class):
        """加入会话"""
        if self._limit and len(self._connections) >= self._limit:
            raise RuntimeWarning(f'ws connections out of limit, {key} append failed!')

        assert hasattr(message_handle_class, 'on_message') and hasattr(message_handle_class, 'hello')

        async with self._lock:

            if key in self._connections:
                await self._connections[key].close()

            self._connections[key] = ws
            self._message_handlers[key] = message_handle_class

    async def handle_message(self, key, receive_func='receive_text'):
        """处理会话循环"""
        try:
            ws: WebSocket = self._connections[key]
            await ws.accept()

            if not hasattr(ws, receive_func):
                await ws.close()
                raise AttributeError(f'Attribute "{receive_func}" not found')

            receive = getattr(ws, receive_func)
            message_handler = self._message_handlers[key]
            count = 0
            await message_handler.hello(ws, count)
            while True:
                try:
                    message = await asyncio.wait_for(receive(), self._heartbeat_timeout)
                except asyncio.TimeoutError:
                    count += 1
                    if count >= self._timeout_count:
                        await ws.close()

                        raise WebSocketDisconnect()

                    await message_handler.hello(key, ws, count)
                    continue

                count = 0
                await message_handler.on_message(key, ws, message)

        except WebSocketDisconnect:
            self._connections.pop(key)
            self._message_handlers.pop(key)
            Utils.log.info(f'ws:[{key}] disconnected')

        except Exception:
            Utils.log.error(traceback.format_exc())

    def get_client(self, key):
        return self._connections.get(key)

    async def send_message(self, key, message):
        """根据key发送消息"""

        ws = self.get_client(key)
        if not ws or ws.client_state == WebSocketState.DISCONNECTED:
            Utils.log.warning(f'ws:[{key}] maybe disconnected, can not send message')
            return False

        try:

            if isinstance(message, bytes):
                await ws.send_bytes(message)
            elif isinstance(message, str):
                await ws.send_text(message)
            elif isinstance(message, (list, dict)):
                await ws.send_json(message)
            else:
                await ws.send(message)

            return True

        except WebSocketDisconnect:
            Utils.log.error(f'ws:[{key}] disconnected, send message failed')

        except Exception:
            Utils.log.error(traceback.format_exc())

        return False


class MessageHandler:

    @staticmethod
    async def hello(key, ws, count):

        pass

    @staticmethod
    async def on_message(key, ws, message):

        pass

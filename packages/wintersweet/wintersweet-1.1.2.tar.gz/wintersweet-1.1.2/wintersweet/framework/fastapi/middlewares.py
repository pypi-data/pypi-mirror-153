# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'  # copy

from contextvars import ContextVar

from starlette.types import ASGIApp, Message, Receive, Scope, Send

from wintersweet.utils.base import Utils

REQUEST_ID_CONTEXT = ContextVar(r'request_id')


class RequestIDMiddleware:

    @staticmethod
    def get_request_id():

        request_id = REQUEST_ID_CONTEXT.get(None)

        if request_id is None:
            Utils.log.warning(r'RequestIDMiddleware is not enabled!')

        return request_id

    def __init__(self, app: ASGIApp) -> None:

        self._app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:

        responder = _Response(self._app)

        await responder(scope, receive, send)


class _Response:

    def __init__(self, app: ASGIApp):

        self._app = app
        self._send = None

        self._request_id = Utils.uuid.uuid1().hex

        REQUEST_ID_CONTEXT.set(self._request_id)

    async def __call__(self, scope: Scope, receive: Receive, send: Send):

        self._send = send

        await self._app(scope, receive, self.send)

    async def send(self, message: Message) -> None:

        message.setdefault(r'headers', [])

        message[r'headers'].append((b'x-timestamp', str(Utils.timestamp()).encode(r'latin-1')))
        message[r'headers'].append((b'x-request-id', self._request_id.encode(r'latin-1')))

        await self._send(message)

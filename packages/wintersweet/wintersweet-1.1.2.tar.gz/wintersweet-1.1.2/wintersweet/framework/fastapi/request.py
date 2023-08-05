
__author__ = r'wsb310@gmail.com'  # copy

import fastapi
from starlette.concurrency import run_in_threadpool
from starlette.routing import iscoroutinefunction_or_partial

from starlette.types import Receive, Scope, Send, ASGIApp

from wintersweet.framework.fastapi.middlewares import RequestIDMiddleware
from wintersweet.framework.fastapi.response import Response, ErrResponse
from wintersweet.utils.base import Utils


class APIRoute(fastapi.routing.APIRoute):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.app = self.request_response()

    async def prepare(self, request):

        pass

    def request_response(self) -> ASGIApp:

        func = self.get_route_handler()

        is_coroutine = iscoroutinefunction_or_partial(func)

        async def app(scope: Scope, receive: Receive, send: Send) -> None:
            request = Request(scope, receive, send, self)

            try:

                await self.prepare(request)

                if is_coroutine:
                    response = await func(request)
                else:
                    response = await run_in_threadpool(func, request)

                await response(scope, receive, send)

            except ErrResponse as err:

                Utils.log.warning(f'ErrResponse: {request.path}\n{err}\n{request.debug_info}')

                await err(scope, receive, send)

        return app


class Request(fastapi.Request):

    def __init__(self, scope: Scope, receive: Receive, send: Send, api_route: APIRoute):

        super().__init__(scope, receive, send)

        self._api_route = api_route

        self._request_id = RequestIDMiddleware.get_request_id()

    @property
    def request_id(self):

        return self._request_id

    @property
    def debug_info(self):

        return {
            'request_id': self._request_id,
            'type': self.scope.get(r'type'),
            'http_version': self.scope.get(r'http_version'),
            'server': self.scope.get(r'server'),
            'client': self.scope.get(r'client'),
            'scheme': self.scope.get(r'scheme'),
            'method': self.scope.get(r'method'),
            'root_path': self.scope.get(r'root_path'),
            'path': self.scope.get(r'path'),
            'query_string': self.scope.get(r'query_string'),
            'headers': self.scope.get(r'headers'),
        }

    @property
    def route(self):

        return self._api_route

    @property
    def path(self):

        return self._api_route.path

    @property
    def tags(self):

        return self._api_route.tags

    @property
    def referer(self):

        return self.headers.get(r'Referer')

    @property
    def client_ip(self):

        return self.x_forwarded_for or self.client_host

    @property
    def client_host(self):

        return self.headers.get(r'X-Real-IP', self.client.host)

    @property
    def x_forwarded_for(self):

        return self.headers.get(r'X-Forwarded-For', r'').split(',')[0]

    @property
    def content_type(self):

        return self.headers.get(r'Content-Type')

    @property
    def content_length(self):

        result = self.headers.get(r'Content-Length', r'')

        return int(result) if result.isdigit() else 0

    def get_header(self, name, default=None):

        return self.headers.get(name, default)


class APIRouter(fastapi.APIRouter):

    def __init__(
            self,
            *,
            prefix=r'',
            default_response_class=Response,
            route_class=APIRoute,
            **kwargs
    ):

        super().__init__(
            prefix=prefix,
            default_response_class=default_response_class,
            route_class=route_class,
            **kwargs
        )
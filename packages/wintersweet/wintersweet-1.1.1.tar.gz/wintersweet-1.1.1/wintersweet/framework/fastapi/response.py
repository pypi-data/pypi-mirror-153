from enum import Enum
from fastapi.responses import UJSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from wintersweet.framework.fastapi.middlewares import RequestIDMiddleware


class Response(UJSONResponse):
    def __init__(self, content=None, code=0, status_code=200, extra=None, *args, **kwargs):
        if isinstance(code, Enum):
            code = code.value
        self._code = code
        self._msg = None
        try:
            self._msg = self.build_msg()
        except Exception:
            if code == 0:
                self._msg = 'Success'
            else:
                self._msg = 'Unknown Error'

        self._data = content
        self._extra = extra
        self._request_id = RequestIDMiddleware.get_request_id()

        super().__init__(content=content, status_code=status_code, *args, **kwargs)

    def build_msg(self):
        raise InterruptedError()

    @property
    def data(self):
        return self._data

    def render(self, content):
        return super().render(
            dict(code=self._code, data=content, msg=self._msg, request_id=self._request_id, extra=self._extra)
        )

    def __bool__(self):

        return self._code == 0


class HTTP404Response(Response):
    def __init__(self):
        super(HTTP404Response, self).__init__(code=404, status_code=404)

    def build_msg(self):
        return r'Not Found'


class HTTP405Response(Response):
    def __init__(self):
        super(HTTP405Response, self).__init__(code=405, status_code=405)

    def build_msg(self):
        return r'Method Not Allowed'


class HTTP400Response(Response):
    def __init__(self, content=None, headers=None):
        super(HTTP400Response, self).__init__(
            content=content,
            code=400,
            status_code=HTTP_400_BAD_REQUEST,
            headers=headers
        )

    def build_msg(self):
        return r'Invalid Arguments'


class HTTP500Response(Response):
    def __init__(self, content=None, headers=None):
        super(HTTP500Response, self).__init__(
            content=content,
            code=500,
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            headers=headers
        )

    def build_msg(self):
        return r'Service Unavailable'


class HTTPExceptionResponse(Response):
    def __init__(self, status_code=503, detail='Service Unavailable', headers=None):
        super(HTTPExceptionResponse, self).__init__(
            code=status_code,
            status_code=status_code,
            headers=headers
        )
        self.detail = detail

    def build_msg(self):
        return self.detail


class ErrResponse(Response, Exception):
    pass

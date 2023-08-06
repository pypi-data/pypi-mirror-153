import functools
import os
import traceback
from typing import Optional

import aiofiles
from aiohttp import ClientResponse
from aiohttp.typedefs import DEFAULT_JSON_DECODER, JSONDecoder

from wintersweet.utils.base import Utils


class BaseResponse:
    def __init__(self, client_response: ClientResponse):

        self._client_response = client_response
        self._parsed = False
        self._success = False
        self._status_code = None

    @property
    def response(self):
        return self._client_response

    @property
    def parsed(self):
        return self._parsed

    @property
    def success(self):
        return self._client_response.status < 400

    @property
    def status_code(self):
        return self._client_response.status

    @property
    def headers(self):
        return self._client_response.headers

    @property
    def raw_headers(self):
        return self._client_response.raw_headers

    @property
    def request(self):
        return self._client_response.request_info

    def __await__(self):

        raise NotImplementedError()

    def __repr__(self):
        return f'<{self.__class__.__name__} [{self.status_code}]>'


class HTTPResponse(BaseResponse):

    def __init__(self, client_response: ClientResponse):

        super().__init__(client_response)
        self._content = None
        self._encoding = None

    def __await__(self):
        if not self.parsed:
            self._content = yield from self._client_response.read().__await__()
            self._encoding = self._client_response.get_encoding()
            self._client_response.release()
            self._parsed = True

        return self

    @property
    def text(self):
        return self._content.decode(self._encoding)

    @property
    def content(self):
        return self._content

    def get_text(self, encoding: Optional[str] = None):
        return self._content.decode(encoding or self._encoding)

    def json(self, encoding: Optional[str] = None, loads: JSONDecoder = DEFAULT_JSON_DECODER):
        bytes_data = self._content.strip()

        return loads(bytes_data.decode(encoding or self._encoding))


class DownloadResponse(BaseResponse):

    def __init__(self, file_path, client_response: ClientResponse):
        super().__init__(client_response)
        self._file = file_path

    def __await__(self):
        if not self._parsed:

            w = yield from aiofiles.open(self._file, "wb").__await__()
            try:
                while True:
                    chunk = yield from self._client_response.content.read(65535).__await__()
                    if not chunk:
                        break
                    yield from w.write(chunk)
                self._parsed = True

            except BaseException:
                Utils.log.error(traceback.format_exc())

            finally:
                yield from w.close()

            if not self._parsed:
                os.remove(self._file)

        return self


http_response_partial = functools.partial(HTTPResponse)

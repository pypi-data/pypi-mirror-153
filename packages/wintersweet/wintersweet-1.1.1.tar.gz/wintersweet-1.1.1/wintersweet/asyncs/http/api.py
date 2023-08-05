# -*- coding: utf-8 -*-

import functools
import traceback
import aiohttp

from wintersweet.utils.base import Utils
from wintersweet.asyncs.http.default import DEFAULT_SESSION_ARGS, DEFAULT_SSL_CONTEXT, DEFAULT_DOWNLOAD_TIMEOUT
from wintersweet.asyncs.http.utils import _build_form_data, _file_sender
from wintersweet.asyncs.http.response import HTTPResponse, DownloadResponse, http_response_partial


async def request_ws(url, handle_response_class, **kwargs):
    resp = None
    try:

        async with aiohttp.ClientSession(**DEFAULT_SESSION_ARGS) as session:

            kwargs.setdefault('ssl', DEFAULT_SSL_CONTEXT)

            async with session.ws_connect(method=aiohttp.hdrs.METH_GET, url=url, **kwargs) as response:

                resp = await handle_response_class(response)

            Utils.log.info(f'ws {url} closed')

    except Exception:

        Utils.log.error(traceback.format_exc())

    return resp


async def request(method, url, handle_response_class=http_response_partial, **kwargs):
    """
    Usage::

      >>> from wintersweet.asyncs.http import api
      >>> req = await api.request('GET', 'https://httpbin.org/get')
      >>> req
      <HTTPResponse [200]>
    """
    resp = None
    try:

        async with aiohttp.ClientSession(**DEFAULT_SESSION_ARGS) as session:

            kwargs.setdefault('ssl', DEFAULT_SSL_CONTEXT)

            async with session.request(method=method, url=url, **kwargs) as response:

                resp = await handle_response_class(response)

            Utils.log.info(f'{method.upper()} {url} => status:{resp.status_code}')

    except aiohttp.ClientResponseError as err:

        Utils.log.error(f"{method.upper()} {url} status:{err.status}")

    except Exception:
        
        Utils.log.error(traceback.format_exc())

    return resp


async def get(url, params=None, **kwargs) -> HTTPResponse:
    """便捷的aiohttp GET请求，kwargs兼容aiohttp ClientSession.request参数"""
    return await request(aiohttp.hdrs.METH_GET, url, params=params, **kwargs)


async def options(url, **kwargs) -> HTTPResponse:
    """便捷的aiohttp OPTIONS请求，kwargs兼容aiohttp ClientSession.request参数"""
    return await request(aiohttp.hdrs.METH_OPTIONS, url, **kwargs)


async def head(url, **kwargs) -> HTTPResponse:
    """便捷的aiohttp HEAD请求，kwargs兼容aiohttp ClientSession.request参数"""
    kwargs.setdefault('allow_redirects', False)
    return await request(aiohttp.hdrs.METH_HEAD, url, **kwargs)


async def post(url, data=None, files=None, json=None, **kwargs) -> HTTPResponse:
    """便捷的aiohttp POST请求，kwargs兼容aiohttp ClientSession.request参数"""
    if files:
        # [(name, (filename, open(file_path, 'rb'))), ....]

        data = _build_form_data(data, files)
    kwargs['data'] = data
    return await request(aiohttp.hdrs.METH_POST, url, json=json, **kwargs)


async def put(url, data=None, files=None, json=None, **kwargs) -> HTTPResponse:
    """便捷的aiohttp PUT请求，kwargs兼容aiohttp ClientSession.request参数"""
    if files:
        # [(name, (filename, open(file_path, 'rb'))), ....]

        data = _build_form_data(data, files)
    kwargs['data'] = data

    return await request(aiohttp.hdrs.METH_PUT, url, json=json, **kwargs)


async def patch(url, data=None, files=None, json=None, **kwargs) -> HTTPResponse:
    """便捷的aiohttp PATCH请求，kwargs兼容aiohttp ClientSession.request参数"""
    if files:
        # [(name, (filename, open(file_path, 'rb'))), ....]

        data = _build_form_data(data, files)
    kwargs['data'] = data
    return await request(aiohttp.hdrs.METH_PATCH, url, json=json, **kwargs)


async def delete(url, **kwargs) -> HTTPResponse:
    """便捷的aiohttp DELETE请求，kwargs兼容aiohttp ClientSession.request参数"""
    return await request(aiohttp.hdrs.METH_DELETE, url, **kwargs)


async def request_stream(url, file_path, method=aiohttp.hdrs.METH_POST, **kwargs):
    """流式传输大文件"""
    return await request(method, url=url, data=_file_sender(file_path), **kwargs)


async def download(url, file_path, method=aiohttp.hdrs.METH_GET, **kwargs) -> DownloadResponse:
    """文件下载"""
    kwargs.setdefault('timeout', DEFAULT_DOWNLOAD_TIMEOUT)

    return await request(
        method=method,
        url=url,
        handle_response_class=functools.partial(DownloadResponse, file_path),
        **kwargs
    )

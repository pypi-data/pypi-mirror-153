import os
import re
import xml
import sys
import pytz
import math
import time
import uuid
import types
import random
import socket
import loguru
import hashlib
import asyncio
import textwrap
import datetime
import binascii
import traceback
import itertools
import functools
import xmltodict


def install_uvloop():
    """安装uvloop
    """

    try:
        import uvloop
    except ModuleNotFoundError:
        Utils.log.warning(f'uvloop is not supported (T＿T)')
    else:
        uvloop.install()
        Utils.log.success(f'uvloop {uvloop.__version__} installed')


class Utils:

    os = os
    log = loguru.logger
    sys = sys
    math = math
    uuid = uuid
    time = time
    random = random
    hashlib = hashlib
    asyncio = asyncio
    datetime = datetime
    textwrap = textwrap
    traceback = traceback
    itertools = itertools
    functools = functools

    @staticmethod
    def package_task(func, *args, **kwargs):
        if asyncio.iscoroutinefunction(func):
            if args or kwargs:
                return Utils.functools.partial(func, *args, **kwargs)
            else:
                return func
        else:
            async def cro_func():
                return func(*args, **kwargs)

            return cro_func()

    @staticmethod
    @types.coroutine
    def wait_frame(count=10):
        """暂停指定帧数
        """
        for _ in range(max(1, count)):
            yield

    @classmethod
    def ip2int(cls, val):

        try:
            return int(binascii.hexlify(socket.inet_aton(val)), 16)
        except socket.error:
            return int(binascii.hexlify(socket.inet_pton(socket.AF_INET6, val)), 16)

    @classmethod
    def int2ip(cls, val):

        try:
            return socket.inet_ntoa(binascii.unhexlify(r'%08x' % val))
        except socket.error:
            return socket.inet_ntop(socket.AF_INET6, binascii.unhexlify(r'%032x' % val))

    @classmethod
    def time2stamp(cls, time_str, format_type=r'%Y-%m-%d %H:%M:%S', timezone=None):

        if timezone is None:
            return int(datetime.datetime.strptime(time_str, format_type).timestamp())
        else:
            return int(datetime.datetime.strptime(time_str, format_type).replace(tzinfo=pytz.timezone(timezone)).timestamp())

    @classmethod
    def stamp2time(cls, time_int=None, format_type=r'%Y-%m-%d %H:%M:%S', timezone=None):

        if time_int is None:
            time_int = cls.timestamp()

        if timezone is None:
            return time.strftime(format_type, datetime.datetime.fromtimestamp(time_int).timetuple())
        else:
            return time.strftime(format_type, datetime.datetime.fromtimestamp(time_int, pytz.timezone(timezone)).timetuple())

    @staticmethod
    def datetime2time(datetime_time, format_type=r'%Y-%m-%d %H:%M:%S'):
        return time.strftime(format_type, datetime_time.timetuple())

    @classmethod
    def time2datetime(cls, time_str, format_type=r'%Y-%m-%d %H:%M:%S', timezone=None):
        timestamp = cls.time2stamp(time_str, format_type, timezone=timezone)

        if timezone:
            return datetime.datetime.fromtimestamp(timestamp, pytz.timezone(timezone))
        return datetime.datetime.fromtimestamp(timestamp)

    @staticmethod
    def timestamp():
        return int(time.time())

    @staticmethod
    def delta_datetime(
            origin=False,
            add=True,
            **kwargs
    ):
        if add:
            datetime_time = datetime.datetime.now() + datetime.timedelta(**kwargs)
        else:
            datetime_time = datetime.datetime.now() - datetime.timedelta(**kwargs)

        if origin:
            datetime_time = datetime_time.replace(hour=0, minute=0, second=0, microsecond=0)

        return datetime_time

    @staticmethod
    def loop_time():
        """获取当前loop时钟
        """
        loop = asyncio.events.get_event_loop()

        return loop.time()

    @staticmethod
    def format_time(format=r'%Y-%m-%d %H:%M:%S'):
        return time.strftime(format, datetime.datetime.now().timetuple())

    @classmethod
    def re_match(cls, pattern, value):

        result = re.match(pattern, value)

        return result if result else None

    @classmethod
    def xml_encode(cls, dict_val, root_tag=r'root'):

        xml_doc = xml.dom.minidom.Document()

        root_node = xml_doc.createElement(root_tag)
        xml_doc.appendChild(root_node)

        def _convert(_doc, _node, _dict):

            for key, val in _dict.items():

                temp = _doc.createElement(key)

                if isinstance(val, dict):
                    _convert(_doc, temp, val)
                else:
                    temp.appendChild(_doc.createTextNode(str(val)))

                _node.appendChild(temp)

        _convert(xml_doc, root_node, dict_val)

        return xml_doc

    @classmethod
    def xml_decode(cls, val: str):

        return xmltodict.parse(val)

    @classmethod
    def split_int(cls, val, sep=r',', minsplit=0, maxsplit=-1):

        result = [int(item.strip()) for item in val.split(sep, maxsplit) if item.strip().lstrip(r'-').isdigit()]

        fill = minsplit - len(result)

        if fill > 0:
            result.extend(0 for _ in range(fill))

        return result

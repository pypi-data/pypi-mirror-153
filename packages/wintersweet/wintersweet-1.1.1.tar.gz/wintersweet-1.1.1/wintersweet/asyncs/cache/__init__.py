import asyncio
import copy
import functools
import hashlib
import json
import traceback

from wintersweet.asyncs.pool.redis import redis_pool_manager
from wintersweet.utils.base import Utils


class ShareCache:

    """
    并发缓存器
        实现功能：瞬时并发执行某个cro函数，通过计算签名相同时，只执行一次，并且支持缓存到redis以及从redis取
        注意事项：1、当使用ShareCache修饰的函数，其参数需支持json序列化
                当为普通对象时因计算签名不一致将无法起到缓存作用
                2、当使用redis作为缓存介质时，将对返回值进行json序列化，因此返回值仅限基本类型，不可为普通对象
                当缓存反序列化后，原返回值中的tuple类型将映射为list类型返回
                因此，为避免前后调用返回结果不一致，请确保返回值中不包含不可序列化对象或经反序列化不产生结构和类型变化的对象
    Usage::
    >>> @ShareCache(cache_none=True, use_redis=True, ttl=30)
    >>> async def test(*args, **kwargs):
    >>>     ...
    >>>     return [1, 2]   # 建议，序列化反序列化后结构和类型不发生变化，都是list
    >>>     return 1, 2   # 不建议，序列化前是tuple，反序列化后是list，使用缓存时，将导致第一次调用返回tuple，第二次调用从缓存取会得到list

    >>> result = await test(1, 2)
    """

    def __init__(self, tag=None, cache_none=False, use_redis=True, ttl=30):
        """
        :param tag: 被装饰的函数唯一标识，如果tag为None，计算签名将使用函数名作为函数唯一标识
        :param cache_none: 是否缓存返回值None
        :param use_redis: 是否使用缓存
        :param ttl: 缓存时长，单位s
        """
        self._ttl = ttl
        self._cache_none = cache_none
        self._use_redis = use_redis
        self._futures = {}
        self._tag = tag

    def __call__(self, func):

        @functools.wraps(func)
        async def _wrapper(*args, **kwargs):

            func_sign = self._sig(func, *args, **kwargs)
            if func_sign in self._futures:
                f = asyncio.Future()
                self._futures[func_sign].append(f)
            else:
                f = asyncio.create_task(self.wrapper_func(func_sign, func, *args, **kwargs))
                if not f:
                    raise RuntimeError(f'"{func}" is not a cro function')

                self._futures[func_sign] = [f]
                f.add_done_callback(functools.partial(self._set_result, func_sign))

            return await f

        return _wrapper

    def _sig(self, func, *args, **kwargs):
        hash_str = f'{self._tag if self._tag else func.__name__}%@@%{args}%@@%{kwargs}'
        return hashlib.md5(hash_str.encode()).hexdigest()

    def _set_result(self, func_sign, _):

        if func_sign not in self._futures:
            return

        futures = self._futures.pop(func_sign)

        result = futures.pop(0).result()

        for future in futures:
            future.set_result(copy.deepcopy(result))

    async def wrapper_func(self, func_sign, func, *args, **kwargs):

        if not self._use_redis:
            return await func(*args, **kwargs)

        result = None
        async with redis_pool_manager.get_client() as client:

            _result = await client.get(func_sign)
            if _result:
                try:
                    result = json.loads(_result)['result']
                    if self._cache_none:
                        if result is None:
                            return result

                except Exception:
                    Utils.log.warning(f'{self.__class__.__name__} got unexpected result "{_result}"')
                    await client.delete(func_sign)

        if result:
            return result

        result = await func(*args, **kwargs)

        async with redis_pool_manager.get_client() as client:
            try:
                await client.set(func_sign, json.dumps({'result': result}), expire=self._ttl)
            except:
                Utils.log.error(traceback.format_exc())

        return result

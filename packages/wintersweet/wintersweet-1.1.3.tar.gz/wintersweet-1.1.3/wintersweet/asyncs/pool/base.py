import asyncio
import json
import uuid
from contextvars import ContextVar

from aioredis import Redis


class BasePoolManager:
    def __init__(self):
        self._pools = {}
        self._config = {}
        self._ready = False

    def register(self, config):
        assert not self.ready, f'{self.__class__.__name__} already registered'
        self._config = config

    async def initialize(self):

        await self

    def __await__(self):

        raise NotImplementedError()

    def __repr__(self):
        return id(self)

    def __str__(self):
        return json.dumps({
            pool_name: self.pool_status(pool_name)
            for pool_name, pool in self._pools.items()
        }, indent=4, ensure_ascii=False)

    @property
    def ready(self):

        return self._ready

    def get_pool(self, pool_name='default'):
        return self._pools[pool_name]

    def pool_status(self, pool_name='default'):

        raise NotImplementedError()

    def get_client(self, pool_name='default', alone=False) -> Redis:

        return self._pools[pool_name].get_context_manager_client(alone)

    async def close(self):

        raise NotImplementedError()

    async def check_health(self):
        if self._pools:
            return all(await asyncio.gather(*[pool.health() for pool in self._pools.values()]))
        else:
            return True

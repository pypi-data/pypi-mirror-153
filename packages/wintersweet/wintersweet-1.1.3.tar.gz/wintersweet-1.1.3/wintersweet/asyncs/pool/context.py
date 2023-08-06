import asyncio

import aioredis


class _AsyncContextManager:

    def __init__(self, pool, alone=False):

        self._pool = pool
        self._is_ctx = False
        self._alone = alone

    async def __aenter__(self):
        if not self._alone:
            self._client = self._pool.get_context_client()
            if not self._client:
                self._client = await self._pool.get_client()
            else:
                self._is_ctx = True
        else:
            self._client = await self._pool.get_client()

        return self._client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._is_ctx:
            return

        _pool, self._pool = self._pool, None
        _client, self._client = self._client, None

        if hasattr(_client, 'close'):
            res = _client.close()
            if asyncio.iscoroutine(res):
                await res

        if isinstance(_pool, aioredis.ConnectionsPool):
            await _pool.release(_client)

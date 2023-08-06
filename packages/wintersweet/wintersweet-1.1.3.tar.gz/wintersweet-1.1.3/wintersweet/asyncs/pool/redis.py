
import aioredis
import asyncio
import json
import time
import traceback
import uuid
import weakref

from contextvars import ContextVar
from aioredis import Redis, ConnectionsPool

from wintersweet.asyncs.pool.base import BasePoolManager
from wintersweet.asyncs.pool.context import _AsyncContextManager
from wintersweet.asyncs.task.tasks import IntervalTask
from wintersweet.asyncs.tools.circular import AsyncCircularForTimeout, AsyncCircularForSecond
from wintersweet.utils.base import Utils
from wintersweet.utils.errors import catch_error
from wintersweet.utils.metaclass import SafeSingleton


class RedisPool(ConnectionsPool):

    def __init__(self, *args, **kwargs):

        super(RedisPool, self).__init__(*args, **kwargs)
        self._context = ContextVar(f'{self.__class__.__name__}_{uuid.uuid1().hex}', default=None)
        self._name = None

    @property
    def name(self):
        return self._name

    def _echo_pool_info(self):
        free = self.maxsize - self.size + self.freesize
        if free < Utils.math.ceil(self.maxsize / 3):
            Utils.log.warning(
                f'Redis pool not enough ({self._name}): (free:{free}/max:{self.maxsize})'
             )

    def get_context_client(self):
        ref = self._context.get()
        client = None
        if ref is not None:
            _client = ref() or None
            if _client and not _client.closed:
                client = _client
        return client

    async def get_client(self, alone=False):
        if self.closed:
            return
        self._echo_pool_info()
        client = Redis(await self.acquire())
        if not alone:
            self._context.set(weakref.ref(client))

        return client

    async def release(self, client: Redis):
        with catch_error():
            if self.closed:
                return

            client.close()
            await client.wait_closed()
            super().release(client._pool_or_conn)

    def get_context_manager_client(self, alone=False):

        return _AsyncContextManager(self, alone=alone)

    async def health(self):
        try:

            async with self.get_context_manager_client(alone=True) as client:

                await client.ping()
                return True

        except Exception:

            Utils.log.error(traceback.format_exc())

            return False


class MutexLock:
    """基于Redis实现的分布式锁，当await lock.acquire()一旦获取锁成功，会自动触发看门狗，持续对lock进行检查并保持持有
        直到跳出async with管理或者手动调用release()
        使用方法1（建议）：
            async with MutexLock(redis_pool, 'test-key', 60) as lock:
                is_locked = await lock.acquire()
                if is_locked:
                    # do something
                else:
                    # do something

        当你需要在程序生命周期内保持锁占有时，可使用方法2
        使用方法2：
            lock = MutexLock(redis_pool, 'test-key', 60)
            try:
                is_locked = await lock.acquire()
                if is_locked:
                    # do something
                else:
                    # do something
            except Exception as e:
                # do something
            finally:
                await lock.release()
    """

    _renew_script = '''
    if redis.call("get",KEYS[1]) == ARGV[1] and redis.call("ttl",KEYS[1]) > 0 then
        return redis.call("expire",KEYS[1],ARGV[2])
    else
        return 0
    end
    '''

    _unlock_script = '''
    if redis.call("get",KEYS[1]) == ARGV[1] then
        return redis.call("del",KEYS[1])
    else
        return 0
    end
    '''

    def __init__(self, redis_pool: RedisPool, key, expire=60):

        self._redis_pool = redis_pool
        assert expire > 3, '"expire" is too small'
        self._expire = expire
        self._key = key
        self._lock_tag = f'process_lock_{key}'
        self._lock_val = Utils.uuid.uuid1().hex.encode()

        self._locked = False
        self._cache = None
        self._err_count = 0

        # watch dog
        self._watcher = None

    async def __aenter__(self):

        await self._init_conn()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):

        await self.release()

    def __del__(self):
        if self._cache:
            asyncio.create_task(self.release())

    def __repr__(self):
        return f'{self.__class__.__name__}<{self._key}>'

    @property
    def locked(self):
        return self._locked

    async def _do_heartbeat(self):
        """watch dog continuous to refresh the lock"""
        res = await self.acquire(0)
        Utils.log.info(f'{str(self)} Watcher lock result: {res}')

    async def _init_conn(self, reset=False):
        """init redis conn or reset redis conn"""
        try:
            if self._cache is None or reset:
                if reset and self._cache is not None:
                    await self.release()
                self._cache = await self._redis_pool.get_client(alone=True)
                if not self._cache:
                    raise ValueError('can not get redis client')
                self.init_watcher()
                return True
        except Exception:
            Utils.log.error(f'{str(self)} init redis conn error')
            Utils.log.error(traceback.format_exc())

    def init_watcher(self):
        """init watch dog"""
        interval = Utils.math.floor(self._expire / 3)
        self._watcher = IntervalTask(interval or 3, self._do_heartbeat, tag=self.__class__.__name__)

    async def exists(self):
        """check the lock exist or not"""
        await self._init_conn()
        if await self._cache.exists(self._lock_tag):
            return True
        else:
            return False

    async def acquire(self, timeout=0):
        """acquire the lock"""
        assert not self._redis_pool.closed
        try:
            if self._locked:
                self._locked = await self.renew()
            else:
                await self._init_conn()

                params = {
                    r'key': self._lock_tag,
                    r'value': self._lock_val,
                    r'expire': self._expire,
                    r'exist': Redis.SET_IF_NOT_EXIST,
                }

                async for _ in AsyncCircularForTimeout(timeout):

                    if await self._cache.set(**params):
                        self._locked = True

                    if self._locked or timeout == 0:
                        break
            if self._locked and not self._watcher.running:
                self._watcher.start()

            if not self._locked:
                await self.release()

        except aioredis.errors.ConnectionClosedError:
            self._err_count += 1
            Utils.log.error(f'{str(self)} acquire conn closed error')
            if self._err_count >= 3:
                # If the connection is damaged, automatic reset to ensure service resume
                reset_res = await self._init_conn(reset=True)
                if reset_res:
                    self._err_count = 0

        return self._locked

    async def wait(self, timeout=0):

        async for _ in AsyncCircularForTimeout(timeout):

            if not await self.exists():
                return True
        else:
            return False

    async def renew(self):
        """renew the lock when lock held"""
        if self._cache is None:
            self._locked = False

        if self._locked:
            self._locked = False
            if await self._cache.eval(self._renew_script, [self._lock_tag], [self._lock_val, self._expire]):
                self._locked = True
            else:
                self._locked = False

        return self._locked

    async def release(self):
        """release the lock, and stop the watch dog"""
        with catch_error():
            if self._watcher and self._watcher.running:
                self._watcher.stop()
                self._watcher = None
            if self._locked and self._cache:
                await self._cache.eval(self._unlock_script, [self._lock_tag], [self._lock_val])
                self._locked = False

            if self._cache:
                await self._redis_pool.release(self._cache)
                self._cache = None


class FrequencyLimiter:
    DEFAULT_EXPIRE = 60

    def __init__(self, redis_pool: RedisPool, granularity, limit, conn_num=1, alone=False, ntp=None):

        self._redis_pool = redis_pool
        self._granularity = granularity
        self._limit = limit
        self._ntp = ntp
        self._alone = alone
        self._conn_num = conn_num
        self._expire = max([self._granularity, self.DEFAULT_EXPIRE])
        self._clients = []
        self._lock = asyncio.Lock()
        asyncio.create_task(self._init_clients())

    async def _init_clients(self, reset=False):
        async with self._lock:
            if reset:
                for client in self._clients:
                    await self._redis_pool.release(client)
                self._clients = []

            if not self._clients:
                self._clients = await asyncio.gather(
                    *[self._redis_pool.get_client(alone=self._alone) for _ in range(self._conn_num)])

            return self._clients[int(time.time() * 1000) % self._conn_num]

    async def get_client(self):

        if not self._clients:
            await self._init_clients()

        return self._clients[int(time.time() * 1000) % len(self._clients)]

    def generate_key(self, key):

        if self._ntp:
            divide = int(self._ntp.timestamp) // self._granularity
        else:
            divide = int(time.time()) // self._granularity

        return f'{self.__class__.__name__}_{key}_{divide}'

    async def incrby(self, key, incr_num=1):

        res = 0
        for _ in range(3):
            client = await self.get_client()

            try:

                pipeline = client.pipeline()
                _key = self.generate_key(key)

                pipeline.incrby(_key, incr_num)
                pipeline.expire(_key, self._expire)

                res, _ = await pipeline.execute()
                break
            except aioredis.errors.ConnectionClosedError:
                await self._init_clients(reset=True)
                continue

        return res

    async def is_limited(self, key, incr_num=1):

        res = await self.incrby(key, incr_num)
        if res > self._limit:
            return True
        return False

    async def release(self):
        if self._clients:
            for client in self._clients:
                await self._redis_pool.release(client)


class RedisPoolManager(SafeSingleton, BasePoolManager):
    """Redis连接池管理器"""
    def __init__(self):
        super().__init__()
        self._event_bus_pool = {}

    def __await__(self):

        if not self._pools:

            for pool_name, pool_config in self._config.items():
                pool_config.setdefault('pool_cls', RedisPool)
                self._pools[pool_name] = yield from aioredis.create_pool(**pool_config).__await__()
                setattr(self._pools[pool_name], '_name', pool_name)

                Utils.log.success(f'redis pool {self.pool_status(pool_name)} initialized')

            self._ready = True

        return self

    def close(self):
        if not self._pools:
            return
        pools, self._pools = self._pools, {}
        for pool in pools.values():
            pool.close()

    def pool_status(self, pool_name='default'):
        pool = self._pools[pool_name]
        return f'<[{pool_name}] {pool.address} [db:{pool.db}, size:[{pool.minsize}:{pool.maxsize}], free:{pool.freesize}]>'

    def allocate_lock(self, key, expire=60, pool_name='default'):
        assert self._ready, f'{self.__class__.__name__} does not initialize'

        return MutexLock(self._pools[pool_name], key, expire=expire)

    def allocate_limiter(self, pool_name='default', granularity=1, limit=10, conn_num=1, alone=False, ntp=None):
        assert self._ready, f'{self.__class__.__name__} does not initialize'

        return FrequencyLimiter(
            self._pools[pool_name],
            granularity=granularity,
            alone=alone,
            conn_num=conn_num,
            limit=limit,
            ntp=ntp
        )

    def allocate_event_bus(self, pool_name='default', channel_name='default'):
        assert self._ready, f'{self.__class__.__name__} does not initialize'
        assert pool_name in self._pools
        key = f'{pool_name}_|x|x|_{channel_name}'
        if key not in self._event_bus_pool:
            event_bus = RedisEventBus(self._pools[pool_name], channel_name)
            self._event_bus_pool[key] = event_bus

        return self._event_bus_pool[key]


redis_pool_manager = RedisPoolManager()


class RedisEventBus:
    """redis发布|订阅"""
    def __init__(self, redis_pool: RedisPool, channel_name):
        self._redis_pool = redis_pool

        self._channel = f'EVENT_BUS_[{self._redis_pool.name}]_[{channel_name}]'
        self._callbacks = {}

        asyncio.create_task(self._subscribe())

    def add_listener(self, tag: str, callback):
        assert asyncio.iscoroutinefunction(callback), 'callback must be coroutinefunction'
        if tag in self._callbacks:
            self._callbacks[tag].append(callback)
        else:
            self._callbacks[tag] = [callback]

    async def _subscribe(self):
        async for _ in AsyncCircularForSecond():
            if self._redis_pool.closed:
                continue
            async with self._redis_pool.get_context_manager_client(alone=True) as client:

                receiver, = await client.subscribe(self._channel)
                Utils.log.info(f'{self.__class__.__name__} channel({self._channel}) subscribed')

                async for message in receiver.iter():
                    asyncio.create_task(self._broadcast(message))

    async def _broadcast(self, message):

        message_dic = json.loads(message)
        tag = message_dic['tag']
        args = message_dic['args']
        kwargs = message_dic['kwargs']
        if tag in self._callbacks:
            await asyncio.gather(*[callback(*args, **kwargs) for callback in self._callbacks[tag]])

    async def publish(self, tag, *args, **kwargs):

        message = json.dumps(
            {
                'tag': tag,
                'args': list(args),
                'kwargs': kwargs
            }
        )

        async with self._redis_pool.get_context_manager_client() as client:
            await client.publish(self._channel, message)

        Utils.log.info(f'{self._channel } publish message args:{args} kwargs:{kwargs}')



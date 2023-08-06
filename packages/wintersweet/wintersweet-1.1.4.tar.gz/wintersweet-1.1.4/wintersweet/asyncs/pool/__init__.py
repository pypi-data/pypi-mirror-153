import asyncio
import struct
import time

from multiprocessing import shared_memory
from wintersweet.asyncs.task.tasks import IntervalTask
from wintersweet.asyncs.tools.circular import AsyncCircularForSecond
from wintersweet.utils.base import Utils

from .mysql import mysql_pool_manager
from .redis import redis_pool_manager
from .mongo import mongo_pool_manager


class _HealthShareMemory(shared_memory.SharedMemory):
    """健康状态进程间共享内存"""

    def __init__(self, name, create=False):
        super().__init__(name, create, size=8)

    def write(self, val: int):
        bytes_val = struct.pack('l', val)
        self.buf[:8] = bytes_val

    def read(self):
        bytes_val = self.buf[:8]
        return struct.unpack('l', bytes_val)[0]


class HealthChecker:
    """
        单进程服务健康检查器
        循环任务检查自身健康状况 认定节点不健康或者恢复健康往往具有一定滞后性
        Usage::
        >>> from wintersweet.asyncs.pool import HealthChecker

        >>> health_checker = HealthChecker()
        >>> await health_checker.initialize()
        >>> while True:
        >>>     print(health_checker.health)
        >>>     await asyncio.sleep(1)
    """

    def __init__(self, interval=10, timeout=30):
        self._health_interval = interval
        self._health_timeout = timeout
        self._last_check_time = 0
        self._check_task = IntervalTask(self._health_interval, self._check_health)

    async def initialize(self):
        self._check_task.start()
        await self._check_health()

    @property
    def health(self):
        return self._last_check_time + self._health_timeout > time.time()

    def check_list(self):
        return [
            mysql_pool_manager.check_health(),
            mongo_pool_manager.check_health(),
            redis_pool_manager.check_health()
        ]

    async def _check_health(self):
        result = all(await asyncio.gather(
            *self.check_list()
        ))
        if result:
            self._last_check_time = time.time()

        Utils.log.debug(f'check health:{result}')

    def release(self):
        self._check_task.stop()


class ProcessHealthChecker:

    """ 多进程健康状态检查器
        当前节点所有服务进程均健康才会认为节点健康，认定节点不健康或者恢复健康往往具有一定滞后性
        在使用 gunicorn为fastapi工程启用多进程服务时，可为该节点所有进程健康状况提供依据
        原理：
            本进程内循环任务检查自身健康状态
            当自身检查健康时将检查时间戳写入自身维护的共享内存
            读取其他进程维护的共享内存中的时间戳
            当所有时间戳均在超时范围内时，health返回True, 否则返回False

        Usage::
        >>> from wintersweet.asyncs.pool import ProcessHealthChecker

        >>> health_checker = ProcessHealthChecker(process_num=2)
        >>> await initialize()
        >>> while True:
        >>>     print(health_checker.health)
        >>>     await asyncio.sleep(1)
    """

    def __init__(self, process_num: int, interval=10, timeout=30, ntp=None):
        """
        :param process_num: 开启服务的进程数
        :param interval: 定时检查健康时间间隔
        :param timeout:  健康检查超时时间，当有进程汇报的时间戳超时timeout将被认为节点不健康
        :param ntp: ntp服务  带timestamp属性即可
        """
        self._ntp = ntp
        self._process_num = process_num
        self._health_interval = interval
        self._health_timeout = timeout
        self._memory = None
        self._health = False
        self._process_health_memory = {}
        self._check_task = IntervalTask(self._health_interval, self._check_health)

        self._is_init = False

    async def initialize(self):
        self._check_task.start()
        await self._check_health()

    @property
    def timestamp(self):
        if self._ntp is not None:
            return self._ntp.timestamp
        else:
            return int(time.time())

    async def _init_share_memory(self):

        for index in range(self._process_num):
            if index in self._process_health_memory:
                continue
            name = f'HEALTH_CHECKER_MEMORY_{index}'

            memory = None
            if self._memory is None:
                try:
                    memory = _HealthShareMemory(name=name, create=True)
                    self._memory = memory
                except:
                    memory = _HealthShareMemory(name=name)
            else:
                async for _ in AsyncCircularForSecond(max_times=5):
                    try:
                        memory = _HealthShareMemory(name=name)
                        break
                    except:
                        pass
            if memory:
                self._process_health_memory[index] = memory

        if len(self._process_health_memory) == self._process_num:
            self._is_init = True

    @property
    def health(self):

        return self._health

    def check_list(self):
        return [
            mysql_pool_manager.check_health(),
            mongo_pool_manager.check_health(),
            redis_pool_manager.check_health()
        ]

    async def _check_health(self):

        if not self._is_init:
            await self._init_share_memory()

        if self._memory is not None:
            result = await asyncio.gather(
                *self.check_list()
            )
            if all(result):
                self._memory.write(self.timestamp)

        if not self._is_init:
            self._health = False
        else:
            for item in self._process_health_memory.values():
                if item.read() + self._health_timeout < self.timestamp:
                    self._health = False
                    break
            else:
                self._health = True

        Utils.log.debug(f'check health:{self._health}')

    def release(self):
        self._check_task.stop()
        for item in self._process_health_memory.values():
            item.close()

        self._memory.unlink()
        self._process_health_memory.clear()
        self._memory = None
        self._health = False
        self._is_init = False

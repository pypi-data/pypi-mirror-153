import asyncio
import time

import numpy
from ntplib import NTPClient

from wintersweet.asyncs.task.interfaces import TaskInterface
from wintersweet.asyncs.task.tasks import IntervalTask
from wintersweet.utils.base import Utils


class IntervalNTPClient(NTPClient, TaskInterface):

    def __init__(self, interval, host, version=2, port='ntp', timeout=5):

        super(IntervalNTPClient, self).__init__()
        self._running = False
        self._request_args = {
            'host': host,
            'version': version,
            'port': port,
            'timeout': timeout
        }
        self._offset = 0
        self._usability = False
        self._interval_task = IntervalTask(interval, self.run_task, tag=self.__class__.__name__)

    @property
    def offset(self):
        return self._offset

    @property
    def usability(self):
        """可用性标识"""
        return self._usability

    @property
    def timestamp(self):

        return time.time() + self._offset

    def start(self):
        if self._interval_task.running is False:
            self._interval_task.start()
        self._running = True

    def stop(self):
        if self._interval_task.running is True:
            self._interval_task.stop()
        self._running = False

    async def run_task(self):
        loop = asyncio.get_event_loop()
        offsets = []
        for _ in range(5):
            try:
                resp = await loop.run_in_executor(None, self.exec_request)
                offsets.append(resp.offset)
            except Exception as e:
                Utils.log.warning(f'NTP server {self._request_args["host"]} request failed: {e}')

        if offsets:
            self._offset = float(numpy.median(offsets))
            self._usability = True

            Utils.log.info(f'NTP server {self._request_args["host"]} offset {self._offset}')
        else:
            self._usability = False

    def exec_request(self):

        return super().request(**self._request_args)


class IntervalNTPClientManager:
    """多节点共建NTP，分布式高可用"""
    def __init__(self, interval, hosts: list, version=2, port='ntp', timeout=5):

        self._clients = [
            IntervalNTPClient(interval, host=host, version=version, port=port, timeout=timeout)
            for host in hosts
        ]

    @property
    def timestamp(self):
        clients_offset = [client.offset for client in self._clients if client.usability]
        timestamp = time.time()

        if clients_offset:
            timestamp += float(numpy.median(clients_offset))

        return timestamp

    async def initialize(self):

        await asyncio.gather(*[client.run_task() for client in self._clients])
        for client in self._clients:
            client.start()

    async def stop(self):
        _clients, self._clients = self._clients, []
        for client in self._clients:
            client.stop()

from wintersweet.utils.base import Utils


class _AsyncCircular:
    def __init__(self, max_times=None):

        self._current = 0
        self._max_times = max_times

    def __aiter__(self):

        return self

    async def __anext__(self):

        if self._current > 0:

            if self._is_stop():
                raise StopAsyncIteration()

            await self._sleep()

        self._current += 1

        return self._current - 1

    def _is_stop(self):
        return self._max_times and (self._max_times > 0) and (self._max_times <= self._current)

    async def _sleep(self):

        raise InterruptedError()


class AsyncCircularForFrame(_AsyncCircular):
    """帧异步循环器

    提供一个循环体内的代码重复执行管理逻辑，可控制循环次数、执行间隔(LoopFrame)

    async for index in AsyncCircularForFrame():
        pass

    其中index为执行次数，从0开始

    """

    def __init__(self, max_times, interval=0xfff):
        """
        :param max_times: 循环次数
        :param interval: 执行间隔（帧）
        """
        super(AsyncCircularForFrame, self).__init__(max_times)

        self._interval = interval

    async def _sleep(self):
        await Utils.wait_frame(self._interval)


class AsyncCircularForTimeout(_AsyncCircular):
    """异步超时循环器，在超时时间内，以interval为循环间隔"""
    def __init__(self, timeout, interval=0xfff):
        """
        :param timeout: 超时时长
        :param interval: 执行间隔（帧）
        """
        super(AsyncCircularForTimeout, self).__init__()

        self._interval = interval
        self._timeout_time = Utils.loop_time() + timeout

    def _is_stop(self):
        return self._timeout_time < Utils.loop_time()

    async def _sleep(self):
        await Utils.wait_frame(self._interval)


class AsyncCircularForSecond(_AsyncCircular):
    """秒异步循环器

    可控制循环次数、执行间隔(Second)

    async for index in AsyncCircularForSecond():
        pass

    其中index为执行次数，从0开始

    """
    def __init__(self, max_times=None, interval=1):

        super(AsyncCircularForSecond, self).__init__(max_times)
        self._interval = interval

    async def _sleep(self):
        await Utils.asyncio.sleep(self._interval)


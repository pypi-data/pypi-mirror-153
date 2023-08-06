import logging
import pytz

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from wintersweet.asyncs.task.interfaces import TaskInterface
from wintersweet.utils.base import Utils

TIMEZONE = pytz.timezone(Utils.os.getenv('_TIMEZONE', r'Asia/Shanghai'))


logging.getLogger(r'apscheduler').setLevel(logging.WARNING)


class BaseAsyncIOScheduler(AsyncIOScheduler):
    def __init__(self, tag, **kwargs):
        self._tag = tag
        super().__init__(**kwargs)

    @property
    def tag(self):
        return self._tag


class AsyncIOSchedulerManager:
    """线程安全的定时任务管理器"""

    _schedulers = {}

    @classmethod
    def create_scheduler(cls, tag='default'):

        if tag in cls._schedulers:
            return cls._schedulers[tag]

        scheduler = BaseAsyncIOScheduler(
            tag=tag,
            job_defaults={
                r'coalesce': False,
                r'max_instances': 1,
                r'misfire_grace_time': 10
            },
            timezone=TIMEZONE
        )
        result = cls._schedulers.setdefault(tag, scheduler)
        if id(result) == id(scheduler):
            result.start()

        return result

    @classmethod
    def stop(cls):
        _schedulers, cls._schedulers = cls._schedulers, {}
        for scheduler in _schedulers.values():
            scheduler.shutdown()

        cls._schedulers.clear()


class BaseTask(TaskInterface):

    def __init__(self, func, tag='default', *args, **kwargs):
        super(BaseTask, self).__init__()
        self._scheduler = None
        self._tag = tag
        self._func = Utils.package_task(func, *args, **kwargs)
        self._job = None

    @property
    def scheduler(self):
        return self._scheduler

    def start(self):
        if not self._job:
            self._scheduler = AsyncIOSchedulerManager.create_scheduler(self._tag)
            self._job = self._scheduler.add_job(**self._job_args())
            self._running = True
        return self._job

    def stop(self):
        assert self._job is not None, f'{self.__class__.__name__} has no start'
        self._scheduler.remove_job(self._job.id)
        self._job = None
        self._running = False
        return True

    def _job_args(self):

        raise InterruptedError


class IntervalTask(BaseTask):
    """间隔触发任务"""

    def __init__(self, interval: int, func, tag='IntervalTask', *args, **kwargs):
        super(IntervalTask, self).__init__(func, tag=tag, *args, **kwargs)
        self._interval = interval

    def _job_args(self):
        return {
            'func': self._func,
            'trigger': r'interval',
            'seconds': self._interval
        }


class CrontabTask(BaseTask):
    """定时触发任务"""
    def __init__(self, crontab, func, tag='CrontabTask', *args, **kwargs):
        super(CrontabTask, self).__init__(func, tag, *args, **kwargs)
        self._crontab = crontab

    def _job_args(self):
        return {
            'func': self._func,
            'trigger': CronTrigger.from_crontab(self._crontab, TIMEZONE),
        }

# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

import pytz
import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from ..interface import TaskInterface

from .base import Utils, FutureWithTask, catch_error


TIMEZONE = pytz.timezone(r'Asia/Shanghai')


logging.getLogger(r'apscheduler').setLevel(logging.ERROR)


class TaskAbstract(TaskInterface):
    """任务基类
    """

    def __init__(self, scheduler=None):

        global TIMEZONE

        self._scheduler = AsyncIOScheduler(
            job_defaults={
                r'coalesce': False,
                r'max_instances': 1,
                r'misfire_grace_time': 10
            },
            timezone=TIMEZONE
        ) if scheduler is None else scheduler

    @property
    def scheduler(self):

        return self._scheduler

    @staticmethod
    def _func_wrapper(func, *args, **kwargs):

        if Utils.is_coroutine_function(func):

            if args or kwargs:
                return Utils.func_partial(func, *args, **kwargs)
            else:
                return func

        async def _wrapper():
            return func(*args, **kwargs)

        return _wrapper

    def is_running(self):

        return self._scheduler.running

    def start(self):

        return self._scheduler.start()

    def stop(self):

        return self._scheduler.shutdown()

    def add_job(self):

        raise NotImplementedError()

    def remove_job(self, job_id):

        return self._scheduler.remove_job(job_id)

    def remove_all_jobs(self):

        return self._scheduler.remove_all_jobs()


class IntervalTask(TaskAbstract):
    """间隔任务类
    """

    @classmethod
    def create(cls, interval, func, *args, **kwargs):

        inst = cls()

        inst.add_job(interval, func, *args, **kwargs)

        return inst

    def add_job(self, interval, func, *args, **kwargs):

        return self._scheduler.add_job(
            self._func_wrapper(func, *args, **kwargs),
            r'interval', seconds=interval
        )


class CronTask(TaskAbstract):
    """定时任务类
    """

    @classmethod
    def create(cls, crontab, func, *args, **kwargs):

        inst = cls()

        inst.add_job(crontab, func, *args, **kwargs)

        return inst

    def add_job(self, crontab, func, *args, **kwargs):

        return self._scheduler.add_job(
            self._func_wrapper(func, *args, **kwargs),
            CronTrigger.from_crontab(crontab, TIMEZONE)
        )


class DCSCronTask(TaskInterface):

    def __init__(self, redis_pool, name, crontab, func, *args, **kwargs):

        self._name = name

        self._task_lock = redis_pool.get_client().allocate_lock(f'dcs_cron_task/{name}', 60)
        self._task_func = func

        self._heartbeat = IntervalTask.create(30, self._do_heartbeat)
        self._cron_task = CronTask.create(crontab, self._do_job, *args, **kwargs)

    @property
    def name(self):

        return self._name

    async def _do_heartbeat(self):

        resp = await self._check_status()

        Utils.log.debug(f'dcs cron task heartbeat: {self._name} => {resp}')

    async def _check_status(self):

        if await self._task_lock.acquire():
            return True
        else:
            return False

    async def _do_job(self, *args, **kwargs):

        if await self._check_status():

            Utils.log.info(f'dcs cron task start: {self._name}')

            if Utils.is_coroutine_function(self._task_func):
                await self._task_func(*args, **kwargs)
            else:
                self._task_func(*args, **kwargs)

            Utils.log.info(f'dcs cron task finish: {self._name}')

        else:

            Utils.log.debug(f'dcs cron task idle: {self._name}')

    def start(self, min_delay=30, max_delay=60):

        delay = Utils.randint(min_delay, max_delay)

        def _func():
            self._heartbeat.start()
            self._cron_task.start()
            Utils.log.info(f'dcs cron task init: {self._name}, delay: {delay}')

        if delay == 0:
            _func()
        else:
            Utils.call_later(delay, _func)

    def stop(self):

        self._heartbeat.stop()
        self._cron_task.stop()

    def is_running(self):

        return self._cron_task.is_running()


class RateLimiter:
    """流量控制器，用于对计算资源的保护
    添加任务append函数如果成功会返回Future对象，可以通过await该对象等待执行结果
    进入队列的任务，如果触发限流行为会通过在Future上引发CancelledError传递出来
    """

    def __init__(self, running_limit, waiting_limit=0, timeout=0):

        self._running_limit = running_limit

        self._timeout = timeout

        self._running_tasks = set()
        self._waiting_tasks = asyncio.Queue(waiting_limit)

    def _create_task(self, func, *args, **kwargs):

        if len(args) == 0 and len(kwargs) == 0:
            return FutureWithTask(func)
        else:
            return FutureWithTask(Utils.func_partial(func, *args, **kwargs))

    async def append(self, func, *args, **kwargs):

        task = self._create_task(func, *args, **kwargs)

        await asyncio.wait_for(self._waiting_tasks.put(task), self._timeout)

        await self._fill_running_tasks()

        return task

    async def _fill_running_tasks(self):

        loop_time = Utils.loop_time()

        while not self._waiting_tasks.empty() and self._running_limit > len(self._running_tasks):

            with catch_error():

                task = await self._waiting_tasks.get()

                if (self._timeout <= 0) or ((loop_time - task.build_time) < self._timeout):
                    task.add_done_callback(self._done_callback)
                    self._running_tasks.add(task.run())
                else:
                    task.cancel()
                    Utils.log.warning(f'rate limit timeout: {task} build_time:{task.build_time}')

    def _done_callback(self, task):

        if task in self._running_tasks:
            self._running_tasks.remove(task)

        Utils.call_soon(self._fill_running_tasks)

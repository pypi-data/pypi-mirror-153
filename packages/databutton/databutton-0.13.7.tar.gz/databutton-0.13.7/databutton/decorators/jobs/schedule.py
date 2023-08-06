import asyncio
import datetime
import functools
import importlib
import inspect
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, List

import schedule
from dataclasses_json import dataclass_json

from databutton.utils import async_wrap

if TYPE_CHECKING:
    from databutton.utils.build import ArtifactDict


@dataclass
class DatabuttonSchedule:
    # Unique identifier
    uid: str
    # The human readable name for the job
    name: str
    # The actual name of the function
    func_name: str
    # Seconds between runs (first run will be at t0 + seconds)
    seconds: float
    # The path to the .py file where the schedule is defined
    filepath: str
    # The name of the module (i.e jobs.schedule)
    module_name: str
    # Should the job be cancelled on failure
    cancel_on_failure: bool = False
    # Should run immediately after start, then be scheduled
    run_immediately: bool = True

    def to_dict(self):
        return self.to_dict()


_schedules: List[DatabuttonSchedule] = []


def repeat_every(
    seconds: float,
    name: str = None,
    cancel_on_failure: bool = False,
    run_immediately: bool = True,
):
    def wrapper(func):
        filepath = Path(inspect.getfile(func)).relative_to(Path.cwd())
        job_name = name if name is not None else func.__name__
        uid = f"{filepath}-{func.__name__}-{job_name}"
        _schedules.append(
            DatabuttonSchedule(
                uid=uid,
                name=job_name,
                func_name=func.__name__,
                seconds=seconds,
                filepath=str(filepath),
                module_name=inspect.getmodule(func).__name__,
                cancel_on_failure=cancel_on_failure,
                run_immediately=run_immediately,
            )
        )
        return func

    return wrapper


@dataclass_json
@dataclass
class JobRun:
    timestamp: datetime.datetime
    result: Any


class Job(schedule.Job):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.runs: List[JobRun] = []
        self.databutton_schedule: DatabuttonSchedule = None

    def from_databutton_schedule(self, databutton_schedule: DatabuttonSchedule):
        self.databutton_schedule = databutton_schedule

        mod = importlib.import_module(databutton_schedule.module_name)
        func = getattr(mod, databutton_schedule.func_name)

        # Make everything into coroutines
        if not (inspect.iscoroutine(func) or inspect.iscoroutinefunction(func)):
            func = async_wrap(func)
        return self.do(func)

    async def run(self):
        if self.databutton_schedule is None:
            logging.debug("Running job without a databutton schedule, what?")

        if self._is_overdue(datetime.datetime.now()):
            logging.debug("Cancelling job %s", self)
            return schedule.CancelJob

        try:
            ret = await self.job_func()
        except Exception as e:
            import traceback

            logging.error(traceback.format_exc())

            if os.environ.get("SENTRY_DSN"):
                import sentry_sdk

                with sentry_sdk.push_scope() as scope:
                    scope.set_tag("job.uid", self.databutton_schedule.uid)
                    scope.set_extra("job.last_run", self.last_run)
                    scope.set_extra("job.next_run", self.next_run)
                    scope.set_extra("job.nruns", len(self.runs))
                    sentry_sdk.capture_exception(e)

            if self.databutton_schedule.cancel_on_failure:
                print(f"Cancelling job {self.databutton_schedule.name}")
                ret = schedule.CancelJob
            else:
                ret = e  # Or None? Depends on how we use the jobrun history later

        self.last_run = datetime.datetime.now()

        # Only store the last 10 runs for memory reasons
        self.runs.append(JobRun(timestamp=self.last_run, result=ret))
        self.runs = self.runs[-10:]

        self._schedule_next_run()

        if self._is_overdue(datetime.datetime.now()):
            logging.debug("Cancelling job %s", self)
            return schedule.CancelJob
        return ret


def report_exceptions(cancel_on_failure=False, job: Job = None):
    def catch_exceptions_decorator(job_func):
        @functools.wraps(job_func)
        async def wrapper(*args, **kwargs):
            try:
                ret = await job_func(*args, **kwargs)
                return ret
            except Exception as e:
                import traceback

                logging.error(traceback.format_exc())

                if os.environ.get("SENTRY_DSN"):
                    import sentry_sdk

                    with sentry_sdk.push_scope() as scope:
                        scope.set_tag("job.uid", job.uid)
                        scope.set_extra("job.last_run", job.last_run)
                        scope.set_extra("job.next_run", job.next_run)
                        scope.set_extra("job.nruns", len(job.runs))
                        sentry_sdk.capture_exception(e)

                if cancel_on_failure:
                    return schedule.CancelJob
                else:
                    return None  # Just being explicit

        return wrapper

    return catch_exceptions_decorator


class Scheduler(schedule.Scheduler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jobs: List[Job] = []

    async def load_schedules(self, components: "ArtifactDict"):
        should_run_immediately: List[Job] = []
        for sched in components.schedules:
            job = self.every(sched.seconds).seconds.from_databutton_schedule(sched)

            if sched.run_immediately:
                should_run_immediately.append(job)

        async def run_continously():
            await self.run_pending(override=should_run_immediately)
            while True:
                await self.run_pending()
                await asyncio.sleep(1)

        # return scheduler
        return asyncio.create_task(run_continously())

    async def run_pending(self, override: List[Job] = None):
        job_pool = override if override else self.jobs
        force = True if override else False
        runnable_jobs = [job for job in job_pool if job.should_run or force]
        results = await asyncio.gather(*[job.run() for job in sorted(runnable_jobs)])
        for i, ret in enumerate(results):
            if isinstance(ret, schedule.CancelJob) or ret is schedule.CancelJob:
                self.cancel_job(runnable_jobs[i])
        return results

    def every(self, interval=1):
        job = Job(interval, self)
        return job

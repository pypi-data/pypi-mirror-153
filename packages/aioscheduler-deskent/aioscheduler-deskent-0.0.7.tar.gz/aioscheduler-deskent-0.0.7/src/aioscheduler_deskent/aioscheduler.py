"""
Author: Deskent
Version: 0.0.7
"""

import asyncio
import datetime
from dataclasses import dataclass
from typing import Callable, Optional, Coroutine
import logging

from .exceptions import TimeLeft


logger = logging.getLogger('aioscheduler-deskent')


@dataclass
class Scheduler:
    job_func: 'Callable' = None
    job_start_time: datetime = None

    def add_job(self, job: 'Callable', job_start_time: datetime):
        """Adds new instance Job to the jobs list and returns instance of itself"""

        self.job_func = job
        self.job_start_time = job_start_time

        return self

    async def run(self) -> Optional['Coroutine']:
        """Run current job after timeout, returns result of job function"""

        time_to_sleep: int = (self.job_start_time - datetime.datetime.utcnow()).seconds
        if time_to_sleep <= 0:
            logger.warning(f"Cannot run job in past time.")
            raise TimeLeft
        logger.info(f"Task added [{self.job_start_time}]\tTime to sleep [{time_to_sleep}]")
        try:
            await asyncio.gather(
                asyncio.wait_for(asyncio.sleep(time_to_sleep), time_to_sleep + 1),
                asyncio.sleep(1 / 1000)
            )
        except asyncio.TimeoutError as err:
            logger.error(f'Timeout error: {err}')
        result = self.job_func()
        try:
            return await result
        except TypeError:
            return result

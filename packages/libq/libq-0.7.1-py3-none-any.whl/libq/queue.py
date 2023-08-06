import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Union

import orjson
from pydantic import ValidationError
from redis.asyncio import ConnectionPool

from libq import defaults, errors, serializers
from libq.connections import create_pool
from libq.jobs import Job
from libq.types import JobGenericFail, JobPayload, JobRef, JobStatus, Prefixes
from libq.utils import generate_random, now_secs, parse_timeout

# from libq.worker import AsyncWorker


class Queue:

    def __init__(self, name: str, *,
                 conn: Optional[ConnectionPool] = None,
                 default_timeout=defaults.QUEUE_TIMEOUT,
                 queue_wait_ttl=defaults.QUEUE_WAIT_TTL):
        """
        Queue is the main object to send work.

        :param name: name of the queue
        :param conn: an Async redis connection pool
        :param default_timeout: default time could be a string or int
        :param queue_wait_ttl: default time to put jobs in the queue
        """
        self._name = name
        self._default_timeout = parse_timeout(
            default_timeout)
        self.conn = conn or create_pool()
        self._queue_wait_ttl = parse_timeout(queue_wait_ttl)

    @property
    def name(self) -> str:
        _prefix = Prefixes.queue_jobs.value
        return f"{_prefix}{self._name}"

    async def send_job(self, execid: str, *, payload: JobPayload):
        """ Send job payload to redis """
        data = serializers.job_serializer(payload)
        async with self.conn.pipeline() as pipe:
            pipe.sadd(Prefixes.queues_list.value, self.name)
            pipe.setex(f"{Prefixes.job.value}{execid}",
                       self._queue_wait_ttl, data)
            pipe.rpush(self.name, execid)
            result = await pipe.execute()
        return result

    async def enqueue(self,
                      func_name: str, *,
                      jobid=None,
                      execid=None,
                      params: Dict[str, Any] = {},
                      timeout=None,
                      result_ttl=60 * 5,
                      background=False,
                      max_retry=3,
                      ) -> Job:
        """
        Create and enqueue a job into this queue.

        :param func_name: the complete path to the function to be used as string
        :param jobid: an ID to identify this job, this id doesn't will be used
        for executions, only as an Identifier.
        :param execid: This id will be used for execution.
        :param params: The params that should be serialized to the job.
        :param timeout: a timeout value to do the job
        :param result_ttl: How much time store the result
        :param background: if True the task will run in multiprocessing pool
        in background.
        """

        execid = execid or generate_random()
        ts = parse_timeout(timeout) or self._default_timeout

        _now = int(now_secs())
        status = JobStatus.queued.value

        payload = JobPayload(
            func_name=func_name,
            jobid=jobid,
            execid=execid,
            timeout=ts,
            background=background,
            params=params,
            result_ttl=result_ttl,
            status=status,
            created_ts=_now,
            max_retry=max_retry,
            queue=self._name
        )
        await self.send_job(execid, payload=payload)

        return Job(execid, conn=self.conn, payload=payload)

    async def list_enqueued(self, start="0", end="-1") -> List[str]:
        return await self.conn.lrange(self.name, start, end)

    async def list_failed(self) -> List[str]:
        key = f"{Prefixes.queue_failed.value}{self._name}"
        return await self.conn.hkeys(key)

    async def list_workers(self) -> Set[str]:
        # print(f"{Prefixes.queue_workers.value}{self.name}")
        workers = await self.conn.sinter(
            f"{Prefixes.queue_workers.value}{self._name}")
        return workers

    async def get_failed(self, id: str) -> Union[JobPayload, JobGenericFail]:
        data = await self.conn.hget(f"{Prefixes.queue_failed.value}{self._name}", id)
        try:
            obj = serializers.job_deserializer(data)
        except ValidationError:
            obj = serializers.generic_fail_deserializer(data)
        return obj

    async def send_command(self, cmd: str, *, key=None, public: str = "all"):
        key = key or generate_random()
        channel = f"{Prefixes.queues_commands.value}{self._name}"
        msg = serializers.command_serializer(cmd, key=key, public=public)
        await self.conn.publish(channel, msg)
        return key

    # def get_worker(self, worker_id) -> AsyncWorker:
    #    return AsyncWorker(self._name, conn=self.conn, id=worker_id)

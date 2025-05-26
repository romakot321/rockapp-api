from typing import Coroutine

import rq
from src.detector.domain.entities import Job, JobStatus
from src.detector.application.interfaces.queue_service import IQueueService
from src.core.config import settings
import redis


class RQQueueService(IQueueService):
    def __init__(self) -> None:
        self.connection = redis.Redis(host=settings.REDIS_HOST)
        self.queue = rq.Queue(connection=self.connection)

    def enqueue_job(self, method: Coroutine, *method_args, job_id: str | None = None) -> Job:
        job = self.queue.enqueue(method, *method_args, job_id=job_id)
        return self._to_domain(job)

    def get_job(self, job_id: str) -> Job:
        job = rq.job.Job.fetch(job_id, connection=self.connection)
        return self._to_domain(job)

    @staticmethod
    def _to_domain(job: rq.job.Job) -> Job:
        return Job(
            id=job.id,
            status=JobStatus(job.get_status().value),
            result=job.result
        )

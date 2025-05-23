import abc
from types import CoroutineType
from typing import Coroutine

from src.detector.domain.entities import Job


class IQueueService(abc.ABC):
    @abc.abstractmethod
    def enqueue_job(self, method: CoroutineType, *method_args, job_id: str | None = None) -> Job: ...

    @abc.abstractmethod
    def get_job(self, job_id: str) -> Job: ...

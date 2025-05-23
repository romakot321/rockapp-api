from enum import Enum
from uuid import UUID
from pydantic import BaseModel


class JobStatus(str, Enum):
    queued = 'queued'
    finished = 'finished'
    started = 'started'
    failed = 'failed'


class Job(BaseModel):
    id: UUID
    status: JobStatus
    result: str | None = None

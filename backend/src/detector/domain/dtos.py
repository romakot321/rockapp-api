from enum import Enum
from pydantic import BaseModel
from uuid import UUID


class DetectionStatus(str, Enum):
    queued = 'queued'
    finished = 'finished'
    started = 'started'
    failed = 'failed'


class DetectionDTO(BaseModel):
    id: UUID
    status: DetectionStatus
    result: str | None = None

from uuid import UUID

from fastapi import HTTPException
from src.db.exceptions import ModelNotFoundException
from src.rock.application.interfaces.detection_uow import IDetectionUnitOfWork
from src.rock.domain.entities import Detection


class GetRockDetectUseCase:
    def __init__(self, uow: IDetectionUnitOfWork):
        self.uow = uow

    async def execute(self, detection_id: UUID) -> Detection:
        async with self.uow:
            try:
                detection = await self.uow.detections.get_by_pk(detection_id)
            except ModelNotFoundException:
                raise HTTPException(404)
        return detection

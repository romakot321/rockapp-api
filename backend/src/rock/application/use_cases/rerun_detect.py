from uuid import UUID

from fastapi import HTTPException
from src.rock.application.interfaces.detection_uow import IDetectionUnitOfWork
from src.rock.domain.entities import Detection, DetectionStatus, DetectionUpdate


class RerunRockDetectUseCase:
    def __init__(self, detection_uow: IDetectionUnitOfWork):
        self.detection_uow = detection_uow

    async def execute(self, pk: UUID) -> Detection:
        async with self.detection_uow:
            await self._check_can_rerun(pk)
            detection = await self.detection_uow.detections.update_by_pk(
                pk, DetectionUpdate(status=DetectionStatus.queued)
            )
            await self.detection_uow.commit()
        return detection

    async def _check_can_rerun(self, pk: UUID):
        detection = await self.detection_uow.detections.get_by_pk(pk)
        if detection.status in (DetectionStatus.queued, DetectionStatus.started):
            raise HTTPException(400, detail="Detection cannot be rerunned: Previous run not finished yet")
        elif detection.detector_result is None:
            raise HTTPException(400, detail="Detection cannot be rerunned: Previous run did not produce results")

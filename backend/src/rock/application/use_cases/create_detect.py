from fastapi import HTTPException
from src.rock.domain.dtos import RockDetectionCreateDTO
from src.db.exceptions import ModelConflictException
from src.rock.application.interfaces.detection_uow import IDetectionUnitOfWork
from src.rock.domain.entities import Detection, DetectionCreate


class CreateRockDetectUseCase:
    def __init__(self, uow: IDetectionUnitOfWork):
        self.uow = uow

    async def execute(self, dto: RockDetectionCreateDTO) -> Detection:
        request = DetectionCreate(**dto.model_dump())
        async with self.uow:
            try:
                detection = await self.uow.detections.create(request)
            except ModelConflictException as e:
                raise HTTPException(409, detail="Conflict on detection create: " + str(e))
            await self.uow.commit()
        return detection

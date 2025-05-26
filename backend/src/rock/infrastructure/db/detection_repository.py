from typing import Any
from uuid import UUID

from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.exceptions import ModelNotFoundException
from src.db.exceptions import ModelConflictException
from src.rock.infrastructure.db.orm import RockDetectionDB
from src.rock.application.interfaces.detection_repository import IDetectionRepository
from src.rock.domain.entities import Detection, DetectionCreate, DetectionStatus, DetectionUpdate


class PGDetectionRepository(IDetectionRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _flush(self, exc_args: Any):
        try:
            await self.session.flush()
        except IntegrityError as e:
            raise ModelConflictException(RockDetectionDB.__tablename__, (e, exc_args))

    async def get_by_pk(self, pk: UUID) -> Detection:
        model = await self.session.get(RockDetectionDB, pk)
        if model is None:
            raise ModelNotFoundException(RockDetectionDB.__tablename__, pk)
        return self._to_domain(model)

    async def create(self, detection_data: DetectionCreate) -> Detection:
        model = RockDetectionDB(**detection_data.model_dump(exclude_unset=True))

        self.session.add(model)
        await self._flush(detection_data)

        return self._to_domain(model)

    async def update_by_pk(self, pk: UUID, detection_data: DetectionUpdate) -> Detection:
        query = update(RockDetectionDB).filter_by(id=pk).values(**detection_data.model_dump(exclude_unset=True))
        await self.session.execute(query)
        await self._flush((pk, detection_data))
        return await self.get_by_pk(pk)

    @staticmethod
    def _to_domain(model: RockDetectionDB) -> Detection:
        return Detection(
            id=model.id,
            status=DetectionStatus(model.status),
            detector_result=model.detector_result,
            details=model.details,
            rock_id=model.rock_id
        )

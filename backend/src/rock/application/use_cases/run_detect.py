from typing import BinaryIO
from uuid import UUID, uuid4
import asyncio

from loguru import logger

from src.rock.application.interfaces.rock_uow import IRockUnitOfWork
from src.rock.domain.mappers import GoogleDetectionToRockDetectionMapper
from src.rock.application.interfaces.rock_repository import IRockRepository
from src.rock.domain.exceptions import RockDetectionTimeout
from src.rock.application.interfaces.detection_uow import IDetectionUnitOfWork
from src.rock.domain.entities import (
    Detection,
    DetectionCreate,
    DetectionStatus,
    DetectionUpdate,
    Rock,
)
from src.rock.application.interfaces.detect_client import IDetectClient, TDetection


class RunDetectRockUseCase:
    TIMEOUT_SECONDS = 30

    def __init__(
        self,
        detect_client: IDetectClient,
        uow: IDetectionUnitOfWork,
        detection: Detection,
        rock_uow: IRockUnitOfWork,
    ) -> None:
        self.detect_client = detect_client
        self.uow = uow
        self.detection = detection
        self.rock_uow = rock_uow

    async def execute(self, image: BinaryIO) -> Detection:
        try:
            await self.detect_client.create_detection(self.detection.id, image)
            logger.debug(f"Detect run: detection {self.detection.id} created in client")
            detector_result = await self._wait_for_detector_result()
            logger.debug(f"Detect run: detection {self.detection.id} result: {detector_result}")
            rock = await self.rock_uow.rocks.search_by_name(detector_result.lower())
            logger.debug(f"Detect run: detection {self.detection.id} rock founded: {rock}")
        except Exception as e:
            return await self._set_detection_failed(str(e))

        return await self._store_search_result(rock)

    async def _set_detection_failed(self, details: str | None = None) -> Detection:
        async with self.uow:
            detection = await self.uow.detections.update_by_pk(self.detection.id, DetectionUpdate(status=DetectionStatus.failed, details=details))
            await self.uow.commit()
        return detection

    async def _wait_for_detector_result(self) -> str:
        for _ in range(self.TIMEOUT_SECONDS):
            await asyncio.sleep(1)
            result = await self.detect_client.get_detection(self.detection.id)
            if (stored := await self._store_detector_result(result)) is not None:
                return stored.detector_result
        raise RockDetectionTimeout()

    async def _store_search_result(self, result: Rock) -> Detection:
        async with self.uow:
            detection = await self.uow.detections.update_by_pk(
                self.detection.id, DetectionUpdate(rock_id=result.id)
            )
            await self.uow.commit()
        return detection

    async def _store_detector_result(self, result: TDetection) -> Detection | None:
        domain_result = GoogleDetectionToRockDetectionMapper().map_one(result)
        if (
            domain_result.status != DetectionStatus.finished
            or domain_result.detector_result is None
        ):
            return

        detection_data = DetectionUpdate(detector_result=domain_result.detector_result)
        async with self.uow:
            detection = await self.uow.detections.update_by_pk(
                self.detection.id, detection_data
            )
            await self.uow.commit()

        return detection

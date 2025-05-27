from typing import Any, BinaryIO, Generic
from uuid import UUID, uuid4
import asyncio

from loguru import logger

from src.rock.application.interfaces.rock_uow import IRockUnitOfWork
from src.rock.domain.mappers import DetectionResultToRockDetectionMapper
from src.rock.application.interfaces.rock_repository import IRockRepository
from src.rock.domain.exceptions import RockDetectionTimeout, ResultMapError
from src.rock.application.interfaces.detection_uow import IDetectionUnitOfWork
from src.rock.domain.entities import (
    Detection,
    DetectionCreate,
    DetectionStatus,
    DetectionUpdate,
    Rock,
)
from src.rock.application.interfaces.detect_client import IDetectClient, TAdditional, TDetection


class RunDetectRockUseCase(Generic[TDetection, TAdditional]):
    TIMEOUT_SECONDS = 30

    def __init__(
        self,
        detect_client: IDetectClient[TDetection, TAdditional],
        uow: IDetectionUnitOfWork,
        detection: Detection,
        rock_uow: IRockUnitOfWork,
    ) -> None:
        self.detect_client = detect_client
        self.uow = uow
        self.detection = detection
        self.rock_uow = rock_uow

    async def execute(self, image: BinaryIO) -> Detection:
        additional_data = self._get_additional_data()
        try:
            await self.detect_client.create_detection(self.detection.id, image, additional_data)
            logger.debug(f"Detect run: detection {self.detection.id} created in client")
            detector_result = await self._wait_for_detector_result()
            logger.debug(f"Detect run: detection {self.detection.id} result: {detector_result}")
            rock = await self._search_for_rock(detector_result)
            logger.debug(f"Detect run: detection {self.detection.id} rock founded: {rock}")
        except Exception as e:
            logger.exception(e)
            return await self._set_detection_failed(str(e))

        return await self._store_search_result(rock)

    def _get_additional_data(self) -> TAdditional:
        return self.detection.detector_result

    async def _search_for_rock(self, search_data: str) -> Rock | str:
        if "{" in search_data and "}" in search_data:
            return search_data
        async with self.rock_uow:
            rock = await self.rock_uow.rocks.search_by_name(search_data.lower())
        return rock

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

    async def _store_search_result(self, result: Rock | str) -> Detection:
        if isinstance(result, str):
            return self.detection
        async with self.uow:
            detection = await self.uow.detections.update_by_pk(
                self.detection.id, DetectionUpdate(rock_id=result.id, status=DetectionStatus.finished)
            )
            await self.uow.commit()
        return detection

    async def _store_detector_result(self, result: TDetection) -> Detection | None:
        try:
            domain_result = DetectionResultToRockDetectionMapper().map_one(result)
        except ResultMapError:
            return
        if (
            domain_result.status != DetectionStatus.finished
            or domain_result.detector_result is None
        ):
            return

        detection_data = DetectionUpdate(detector_result=domain_result.detector_result)
        async with self.uow:
            self.detection = await self.uow.detections.update_by_pk(
                self.detection.id, detection_data
            )
            await self.uow.commit()

        return self.detection

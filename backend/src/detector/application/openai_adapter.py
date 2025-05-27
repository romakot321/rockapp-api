from typing import BinaryIO
from loguru import logger
from uuid import UUID
from src.detector.domain.dtos import DetectionStatus, DetectionDTO
from src.detector.domain.entities import Job
from src.detector.application.interfaces.queue_service import IQueueService
from src.detector.application.interfaces.storage import IStorage
from src.detector.application.use_cases.run_detect import RunDetectUseCase
from src.rock.application.interfaces.detect_client import IDetectClient, TAdditional, TDetection


class OpenAIDetectorAdapter[TDetection: DetectionDTO, TAdditional: str](IDetectClient):
    def __init__(self, queue_service: IQueueService, storage: IStorage) -> None:
        self.queue_service = queue_service
        self.storage = storage

    async def create_detection(self, detection_id: UUID, image: BinaryIO, additional_data: str | None = None) -> DetectionDTO:
        self.storage.store_file(str(detection_id), image)
        job = self.queue_service.enqueue_job(RunDetectUseCase.execute_openai, str(detection_id), additional_data, job_id=str(detection_id))
        logger.info(f"Queued rock detection {detection_id}")
        return self._to_dto(job)

    async def get_detection(self, detection_id: UUID) -> DetectionDTO:
        job = self.queue_service.get_job(str(detection_id))
        return self._to_dto(job)

    def _to_dto(self, job: Job) -> DetectionDTO:
        return DetectionDTO(
            id=job.id,
            status=DetectionStatus(job.status.value),
            result=job.result
        )


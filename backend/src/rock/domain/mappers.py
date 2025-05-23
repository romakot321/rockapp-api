from src.rock.domain.entities import Detection as RockDetection, DetectionStatus as RockDetectionStatus
from src.detector.domain.dtos import DetectionDTO as GoogleDetection


class GoogleDetectionToRockDetectionMapper:
    def map_one(self, model: GoogleDetection) -> RockDetection:
        return RockDetection(
            id=model.id,
            status=RockDetectionStatus(model.status.value),
            detector_result=model.result
        )

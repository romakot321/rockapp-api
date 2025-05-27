from enum import Enum
from typing import Any
from src.rock.domain.exceptions import ResultMapError
from src.rock.domain.entities import Detection as RockDetection, DetectionStatus as RockDetectionStatus
from src.detector.domain.dtos import DetectionDTO as DetectionResult


class DetectionResultSource(str, Enum):
    gcloud = "gcloud"
    openai = "openai"


class DetectionResultToRockDetectionMapper:
    def __init__(self, source: DetectionResultSource | None = None) -> None:
        self.source = source

    def map_one(self, model: DetectionResult) -> RockDetection:
        self.source = self._define_source(model)

        if self.source == DetectionResultSource.gcloud:
            return self._map_gcloud(model)
        elif self.source == DetectionResultSource.openai:
            return self._map_openai(model)

        raise ResultMapError("Failed to map detection result: Undefined result source")

    def _map_openai(self, model: DetectionResult) -> RockDetection:
        return RockDetection(
            id=model.id,
            status=RockDetectionStatus(model.status.value),
            detector_result=model.result
        )

    def _map_gcloud(self, model: DetectionResult) -> RockDetection:
        return RockDetection(
            id=model.id,
            status=RockDetectionStatus(model.status.value),
            detector_result=model.result
        )

    def _define_source(self, model: DetectionResult) -> DetectionResultSource | None:
        if self.source is not None:
            return self.source
        if not isinstance(model.result, str):
            return None
        if model.result.startswith("{") and model.result.endswith("}"):  # If it's dumped json
            return DetectionResultSource.openai
        return DetectionResultSource.gcloud

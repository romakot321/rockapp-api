from google.cloud import vision
from google.cloud.vision_v1 import types

from src.detector.application.interfaces.client import IDetectorClient, TAdditional, TResult
from src.detector.domain.exceptions import DetectionError


class GoogleDetector[TResult: str, TAdditional: None](IDetectorClient):
    def __init__(self) -> None:
        self.client = vision.ImageAnnotatorAsyncClient()

    async def execute(self, image_content: bytes, additional_data: None) -> str:
        requests = [
            types.AnnotateImageRequest(
                image=vision.Image(content=image_content),
                features=[types.Feature(type=vision.Feature.Type.LABEL_DETECTION)],
            )
        ]
        response = (
            await self.client.batch_annotate_images(requests=requests)
        ).responses[0]

        if response.error.message:
            raise DetectionError(response.error.message)
        return max(response.label_annotations, key=lambda i: i.score).description

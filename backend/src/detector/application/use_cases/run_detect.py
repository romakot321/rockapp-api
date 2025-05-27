from loguru import logger
from src.detector.infrastructure.openai.detector import OpenAIDetector
from src.detector.infrastructure.openai.responses import OpenAIDetectionResponse
from src.detector.application.interfaces.storage import IStorage
from src.detector.domain.exceptions import DetectionError
from src.detector.infrastructure.localstorage import LocalStorage
from src.detector.application.interfaces.client import IDetectorClient, TAdditional, TResult
from src.detector.infrastructure.gcloud.detector import GoogleDetector


class RunDetectUseCase:
    def __init__(self, client: IDetectorClient, storage: IStorage) -> None:
        self.client = client
        self.storage = storage

    async def execute(self, image_filename: str, additional_data: TAdditional) -> TResult:
        logger.info("Started detection")
        image_content = self._get_image_content(image_filename)
        result = await self.client.execute(image_content, additional_data)
        logger.info(f"Detection finished: {result}")
        return result

    def _get_image_content(self, image_filename: str) -> bytes:
        try:
            file = self.storage.read_file(image_filename)
        except FileNotFoundError:
            raise DetectionError("Input image not found")
        return file.read()

    @classmethod
    async def execute_google(cls, image_filename: str, additional_data: None) -> str:
        self = cls(client=GoogleDetector(), storage=LocalStorage())
        return await self.execute(image_filename, additional_data)

    @classmethod
    async def execute_openai(cls, image_filename: str, additional_data: str | None) -> OpenAIDetectionResponse:
        self = cls(client=OpenAIDetector(), storage=LocalStorage())
        return await self.execute(image_filename, additional_data)

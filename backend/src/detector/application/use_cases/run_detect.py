from loguru import logger
from src.detector.application.interfaces.storage import IStorage
from src.detector.domain.exceptions import DetectionError
from src.detector.infrastructure.localstorage import LocalStorage
from src.detector.application.interfaces.client import IDetectorClient
from src.detector.infrastructure.gcloud.detector import GoogleDetector


class RunDetectUseCase:
    def __init__(self, client: IDetectorClient[str], storage: IStorage) -> None:
        self.client = client
        self.storage = storage

    async def execute(self, image_filename: str) -> str:
        logger.info("Started detection")
        image_content = self._get_image_content(image_filename)
        result = await self.client.execute(image_content)
        logger.info(f"Detection finished: {result}")
        return result

    def _get_image_content(self, image_filename: str) -> bytes:
        try:
            file = self.storage.read_file(image_filename)
        except FileNotFoundError:
            raise DetectionError("Input image not found")
        return file.read()

    @classmethod
    async def execute_google(cls, image_filename: str) -> str:
        self = cls(client=GoogleDetector(), storage=LocalStorage())
        return await self.execute(image_filename)

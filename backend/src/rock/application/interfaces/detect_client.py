import abc
from typing import BinaryIO, Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel

TDetection = TypeVar("TDetection", bound=BaseModel)


class IDetectClient(abc.ABC, Generic[TDetection]):
    @abc.abstractmethod
    async def create_detection(self, detection_id: UUID, image: BinaryIO) -> TDetection: ...

    @abc.abstractmethod
    async def get_detection(self, detection_id: UUID) -> TDetection: ...

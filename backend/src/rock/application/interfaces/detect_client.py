import abc
from typing import BinaryIO, Generic, Optional, TypeVar
from uuid import UUID

from pydantic import BaseModel

TDetection = TypeVar("TDetection", bound=BaseModel)
TAdditional = TypeVar("TAdditional")


class IDetectClient(abc.ABC, Generic[TDetection, TAdditional]):
    @abc.abstractmethod
    async def create_detection(self, detection_id: UUID, image: BinaryIO, additional_data: Optional[TAdditional]) -> TDetection: ...

    @abc.abstractmethod
    async def get_detection(self, detection_id: UUID) -> TDetection: ...

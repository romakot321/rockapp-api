import abc
from typing import Generic, TypeVar

TResult = TypeVar("TResult")


class IDetectorClient(abc.ABC, Generic[TResult]):
    @abc.abstractmethod
    async def execute(self, image_content: bytes) -> TResult: ...

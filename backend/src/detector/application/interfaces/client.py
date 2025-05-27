import abc
from typing import Generic, TypeVar

TResult = TypeVar("TResult")
TAdditional = TypeVar("TAdditional")


class IDetectorClient(abc.ABC, Generic[TResult, TAdditional]):
    @abc.abstractmethod
    async def execute(self, image_content: bytes, additional_data: TAdditional) -> TResult: ...

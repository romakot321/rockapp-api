import abc
from typing import BinaryIO


class IAiohttpClient(abc.ABC):
    @abc.abstractmethod
    async def get(self, url: str, headers: dict | None = None) -> BinaryIO: ...

    # @abc.abstractmethod
    # async def post(self, url: str, json: dict | None = None, body: str | bytes | None = None, headers: dict | None = None) -> dict: ...

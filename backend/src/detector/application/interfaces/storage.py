import abc
from typing import BinaryIO


class IStorage(abc.ABC):
    @abc.abstractmethod
    def store_file(self, filename: str, body: BinaryIO) -> None: ...

    @abc.abstractmethod
    def read_file(self, filename: str) -> BinaryIO: ...

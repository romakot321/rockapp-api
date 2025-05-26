import abc
from typing import BinaryIO


class IImageStorage(abc.ABC):
    @abc.abstractmethod
    async def transfer_image(self, external_url: str, local_filename: str) -> None: ...

    @abc.abstractmethod
    def store_file(self, filename: str, file_body: BinaryIO) -> None: ...

    @abc.abstractmethod
    def read_file(self, filename: str) -> BinaryIO: ...

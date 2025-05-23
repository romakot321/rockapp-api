from typing import BinaryIO
from fastapi_storages import FileSystemStorage

from src.detector.application.interfaces.storage import IStorage


class LocalStorage(IStorage):
    STORAGE_PATH = "storage"

    def __init__(self) -> None:
        self._storage = FileSystemStorage("storage")

    def store_file(self, filename: str, body: BinaryIO) -> None:
        self._storage.write(body, filename)

    def read_file(self, filename: str) -> BinaryIO:
        return self._storage.open(filename)

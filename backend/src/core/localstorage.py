from typing import BinaryIO
from fastapi_storages import FileSystemStorage


class LocalStorage:
    def __init__(self, directory="storage") -> None:
        self.storage = FileSystemStorage(directory)

    def store_file(self, filename: str, file_body: BinaryIO) -> None:
        self.storage.write(file_body, filename)

    def read_file(self, filename: str) -> BinaryIO:
        """Raises FileNotFoundException if file not found"""
        return self.storage.open(filename)

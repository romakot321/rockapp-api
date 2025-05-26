from typing import BinaryIO
from uuid import UUID
from src.rock.application.interfaces.image_storage import IImageStorage


class GetRockImageUseCase:
    def __init__(self, image_storage: IImageStorage) -> None:
        self.image_storage = image_storage

    def execute(self, rock_id: UUID) -> BinaryIO:
        return self.image_storage.read_file(str(rock_id))

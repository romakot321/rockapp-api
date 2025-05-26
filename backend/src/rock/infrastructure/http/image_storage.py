from typing import BinaryIO
from src.rock.application.interfaces.aiohttp_client import IAiohttpClient
from src.rock.application.interfaces.image_storage import IImageStorage
from src.core.localstorage import LocalStorage


class ImageStorage(IImageStorage):
    def __init__(self, client: IAiohttpClient, localstorage=LocalStorage()) -> None:
        self.localstorage = localstorage
        self.client = client

    async def transfer_image(self, external_url: str, local_filename: str) -> None:
        image_body = await self.client.get(external_url)
        self.localstorage.store_file(local_filename, image_body)

    def store_file(self, filename: str, file_body: BinaryIO) -> None:
        self.localstorage.store_file(filename, file_body)

    def read_file(self, filename: str) -> BinaryIO:
        return self.localstorage.read_file(filename)

from io import BytesIO
from typing import BinaryIO
import aiohttp
from src.rock.application.interfaces.aiohttp_client import IAiohttpClient


class AiohttpClient(IAiohttpClient):
    async def get(self, url: str, headers: dict | None = None) -> BinaryIO:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(url, headers=headers)
            resp.raise_for_status()
            body = await resp.read()
        return BytesIO(body)

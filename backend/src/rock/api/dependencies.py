from typing import Annotated

from fastapi import Depends
from src.rock.application.interfaces.image_storage import IImageStorage
from src.rock.infrastructure.http.aiohttp_client import AiohttpClient
from src.rock.infrastructure.http.image_storage import ImageStorage
from src.detector.api.dependencies import GoogleDetectClientDepend, OpenAIDetectClientDepend
from src.rock.application.interfaces.detection_uow import IDetectionUnitOfWork
from src.rock.application.interfaces.rock_uow import IRockUnitOfWork
from src.rock.infrastructure.db.unit_of_work import PGDetectionUnitOfWork
from src.rock.infrastructure.elasticsearch.unit_of_work import ESRockUnitOfWork


def get_detection_uow() -> IDetectionUnitOfWork:
    return PGDetectionUnitOfWork()


def get_rock_uow() -> IRockUnitOfWork:
    return ESRockUnitOfWork()


def get_image_storage() -> IImageStorage:
    return ImageStorage(client=AiohttpClient())


DetectionUoWDepend = Annotated[IDetectionUnitOfWork, Depends(get_detection_uow)]
DetectClientDepend = GoogleDetectClientDepend
DetectGuessClientDepend = OpenAIDetectClientDepend
RockUoWDepend = Annotated[IRockUnitOfWork, Depends(get_rock_uow)]
ImageStorageDepend = Annotated[IImageStorage, Depends(get_image_storage)]

from typing import Annotated

from fastapi import Depends
from src.detector.api.dependencies import GoogleDetectClientDepend
from src.rock.application.interfaces.detection_uow import IDetectionUnitOfWork
from src.rock.application.interfaces.rock_uow import IRockUnitOfWork
from src.rock.infrastructure.db.unit_of_work import PGDetectionUnitOfWork
from src.rock.infrastructure.elasticsearch.unit_of_work import ESRockUnitOfWork


def get_detection_uow() -> IDetectionUnitOfWork:
    return PGDetectionUnitOfWork()


def get_rock_uow() -> IRockUnitOfWork:
    return ESRockUnitOfWork()


DetectionUoWDepend = Annotated[IDetectionUnitOfWork, Depends(get_detection_uow)]
DetectClientDepend = GoogleDetectClientDepend
RockUoWDepend = Annotated[IRockUnitOfWork, Depends(get_rock_uow)]

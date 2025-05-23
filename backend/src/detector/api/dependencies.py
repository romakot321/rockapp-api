from fastapi import Depends
from typing import Annotated

from src.detector.application.adapter import GoogleDetectorAdapter
from src.detector.infrastructure.localstorage import LocalStorage
from src.detector.infrastructure.rq.queue_service import RQQueueService
from src.rock.application.interfaces.detect_client import IDetectClient


def get_google_detector() -> IDetectClient:
    return GoogleDetectorAdapter(RQQueueService(), LocalStorage())


GoogleDetectClientDepend = Annotated[IDetectClient, Depends(get_google_detector)]

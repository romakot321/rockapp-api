from fastapi import Depends
from typing import Annotated

from backend.src.detector.application.openai_adapter import OpenAIDetectorAdapter
from src.detector.application.google_adapter import GoogleDetectorAdapter
from src.detector.infrastructure.localstorage import LocalStorage
from src.detector.infrastructure.rq.queue_service import RQQueueService
from src.rock.application.interfaces.detect_client import IDetectClient


def get_google_detector() -> IDetectClient:
    return GoogleDetectorAdapter(RQQueueService(), LocalStorage())


def get_openai_detector() -> IDetectClient:
    return OpenAIDetectorAdapter(RQQueueService(), LocalStorage())


GoogleDetectClientDepend = Annotated[IDetectClient, Depends(get_google_detector)]
OpenAIDetectClientDepend = Annotated[IDetectClient, Depends(get_openai_detector)]

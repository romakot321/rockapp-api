from io import BytesIO
from uuid import UUID
from fastapi import APIRouter, BackgroundTasks, Depends, File, Header, Query, UploadFile

from src.rock.application.use_cases.get_rock import GetRockUseCase
from src.rock.api.dependencies import DetectClientDepend, DetectionUoWDepend, RockUoWDepend
from src.rock.application.use_cases.add_rock import AddRockUseCase
from src.rock.application.use_cases.create_detect import CreateRockDetectUseCase
from src.rock.application.use_cases.get_detect import GetRockDetectUseCase
from src.rock.application.use_cases.run_detect import RunDetectRockUseCase
from src.rock.domain.dtos import RockDetectionCreateDTO, RockDetectionReadDTO
from src.rock.domain.entities import Rock

router = APIRouter()


@router.post("/detect", response_model=RockDetectionReadDTO)
async def detect_rock(
        detection_uow: DetectionUoWDepend,
        rock_uow: RockUoWDepend,
        detect_client: DetectClientDepend,
        background_tasks: BackgroundTasks,
        image: UploadFile = File(),
        detect_data: RockDetectionCreateDTO = Depends(RockDetectionCreateDTO.as_form),
):
    detection = await CreateRockDetectUseCase(detection_uow).execute(detect_data)
    run_uc = RunDetectRockUseCase(detect_client, detection_uow, detection, rock_uow)
    background_tasks.add_task(run_uc.execute, BytesIO(await image.read()))
    return detection


@router.get("/detect/{detection_id}", response_model=RockDetectionReadDTO)
async def get_detect_rock_status(detection_id: UUID, detection_uow: DetectionUoWDepend):
    detection = await GetRockDetectUseCase(detection_uow).execute(detection_id)
    return detection


@router.get("", response_model=Rock)
async def get_rock(rock_uow: RockUoWDepend, name: str = Query()):
    return await GetRockUseCase(rock_uow).execute_with_name(name)


@router.post("", status_code=201, include_in_schema=False)
async def add_rock(data: Rock, rock_uow: RockUoWDepend, rock_storage_token: str = Header()):
    await AddRockUseCase(rock_uow, rock_storage_token).execute(data)

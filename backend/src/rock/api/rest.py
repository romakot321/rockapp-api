from io import BytesIO
from uuid import UUID
from fastapi import APIRouter, BackgroundTasks, Depends, File, Header, Query, UploadFile
from fastapi.responses import Response

from src.rock.application.use_cases.get_rock_image import GetRockImageUseCase
from src.rock.application.use_cases.get_rock import GetRockUseCase
from src.rock.api.dependencies import DetectClientDepend, DetectionUoWDepend, ImageStorageDepend, RockUoWDepend
from src.rock.application.use_cases.add_rock import AddRockUseCase
from src.rock.application.use_cases.create_detect import CreateRockDetectUseCase
from src.rock.application.use_cases.get_detect import GetRockDetectUseCase
from src.rock.application.use_cases.run_detect import RunDetectRockUseCase
from src.rock.domain.dtos import RockDetectionCreateDTO, RockDetectionReadDTO, RockStoreDTO
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


@router.get("/{rock_id}", response_model=Rock)
async def get_rock(rock_id: UUID, rock_uow: RockUoWDepend):
    return await GetRockUseCase(rock_uow).execute_with_pk(rock_id)


@router.get("", response_model=Rock)
async def search_rock(rock_uow: RockUoWDepend, name: str = Query()):
    return await GetRockUseCase(rock_uow).execute_with_name(name)


@router.post("", status_code=201, include_in_schema=False)
async def add_rock(data: RockStoreDTO, rock_uow: RockUoWDepend, image_storage: ImageStorageDepend, rock_storage_token: str = Header()):
    await AddRockUseCase(rock_uow, image_storage, rock_storage_token).execute(data)


@router.get("/{rock_id}/image", response_class=Response)
async def get_rock_image(rock_id: UUID, image_storage: ImageStorageDepend):
    image = GetRockImageUseCase(image_storage).execute(rock_id)
    return Response(content=image.read(), media_type="image/jpg")

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import Response

from src.user.api.dependencies import UserUoWDepend
from src.user.application.use_cases.create_user import CreateUserUseCase
from src.user.application.use_cases.get_user import GetUserUseCase
from src.user.application.use_cases.list_user_rocks import ListUserRocksUseCase
from src.user.application.use_cases.set_user_avatar import SetUserAvatarUseCase
from src.user.application.use_cases.update_user import UpdateUserUseCase
from src.user.application.use_cases.get_user_avatar import GetUserAvatarUseCase
from src.user.domain.dtos import UserCreateDTO, UserReadDTO, UserReadShortDTO, UserRockDTO, UserUpdateDTO


router = APIRouter()


@router.post("", response_model=UserReadShortDTO)
async def create_user(user_data: UserCreateDTO, user_uow: UserUoWDepend):
    return await CreateUserUseCase(user_uow).execute(user_data)


@router.get("/{user_id}", response_model=UserReadDTO)
async def get_user(user_id: str, user_uow: UserUoWDepend):
    return await GetUserUseCase(user_uow).execute(user_id)


@router.get("/{user_id}/rocks", response_model=list[UserRockDTO])
async def get_user_rocks(user_id: str, user_uow: UserUoWDepend):
    return await ListUserRocksUseCase(user_uow).execute(user_id)


@router.put("/{user_id}/avatar")
async def update_user_avatar(user_id: str, user_uow: UserUoWDepend, file: UploadFile = File()):
    await SetUserAvatarUseCase(user_uow).execute(user_id, await file.read())


@router.get("/{user_id}/avatar", response_model=Response)
async def get_user_avatar(user_id: str, user_uow: UserUoWDepend, file: UploadFile = File()):
    avatar = await GetUserAvatarUseCase(user_uow).execute(user_id)
    return Response(content=avatar, media_type="image/jpg")


@router.patch("/{user_id}", response_model=UserReadShortDTO)
async def update_user(user_id: str, user_data: UserUpdateDTO, user_uow: UserUoWDepend):
    return await UpdateUserUseCase(user_uow).execute(user_id, user_data)

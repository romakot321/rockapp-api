from fastapi import APIRouter

router = APIRouter()


@router.post("")
async def create_user():
    pass


@router.get("")
async def get_user_profile():
    pass

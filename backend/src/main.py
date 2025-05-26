from fastapi import FastAPI

from src.rock.api.rest import router as rock_router
from src.user.api.rest import router as user_router

app = FastAPI(title="RockAPP API")

app.include_router(rock_router, tags=["Rock"], prefix="/api/rock")
app.include_router(user_router, tags=["User"], prefix="/api/user")

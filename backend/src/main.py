from fastapi import FastAPI

from src.rock.api.rest import router as rock_router

app = FastAPI(title="RockAPP API")

app.include_router(rock_router, tags=["Rock"], prefix="/api/rock")

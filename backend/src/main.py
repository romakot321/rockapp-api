from fastapi import FastAPI
from sqladmin import Admin

from src.db.engine import engine
from src.rock.api.rest import router as rock_router
from src.rock.api.admin import RockDetectionAdmin
from src.user.api.rest import router as user_router
from src.user.api.admin import UserRankAdmin, UserAdmin

app = FastAPI(title="RockAPP API")

admin = Admin(app, engine)

app.include_router(rock_router, tags=["Rock"], prefix="/api/rock")
app.include_router(user_router, tags=["User"], prefix="/api/user")

admin.add_view(RockDetectionAdmin)
admin.add_view(UserRankAdmin)
admin.add_view(UserAdmin)

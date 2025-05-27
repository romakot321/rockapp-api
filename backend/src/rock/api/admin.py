from sqladmin import ModelView
from src.rock.infrastructure.db.orm import RockDetectionDB


class RockDetectionAdmin(ModelView, model=RockDetectionDB):
    column_list = "__all__"

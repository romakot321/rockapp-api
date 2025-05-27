from sqladmin import ModelView

from src.user.infrastructure.db.orm import UserDB, UserRankDB


class UserRankAdmin(ModelView, model=UserRankDB):
    column_list = "__all__"


class UserAdmin(ModelView, model=UserDB):
    column_list = [UserDB.id, UserDB.name, UserDB.created_at]

from db.models.UserModel import UserModel
from db.dto import UserCreateDTO, UserPatchDTO
from .base_dao import BaseDAO


class UserDAO(BaseDAO[UserModel, UserCreateDTO, UserPatchDTO, None]):
    pass


user_dao = UserDAO(UserModel)

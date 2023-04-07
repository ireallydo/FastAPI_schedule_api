from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException

from db.models.UserModel import UserModel
from db.dto import *
from .base_dao import BaseDAO


class UserDAO(BaseDAO[UserModel, UserCreateDTO, UserPatchDTO, None]):
    pass


user_dao = UserDAO(UserModel)

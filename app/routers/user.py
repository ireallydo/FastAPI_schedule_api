from typing import List

from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from fastapi import APIRouter
from fastapi_utils.cbv import cbv

from services import user_service

from db.models import *
from db.dto import *
from db.enums import *
from .api_spec import ApiSpec

from db.database import SessionLocal, engine


router = APIRouter(tags=["user"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@cbv(router)
class UserView:
    db: Session = Depends(get_db)

    @router.post(ApiSpec.USERS, status_code=201, response_model=UserDTO)
    def post_user(self, input_data: UserCreateDTO):
        response = user_service.create(self.db, input_data)
        return response

    @router.get(ApiSpec.USERS, status_code=200, response_model=List[UserDTO])
    def get_users(self, skip: int = 0, limit: int = 100):
        response = user_service.get_all(self.db, skip=skip, limit=limit)
        return response

    @router.patch(ApiSpec.USERS, status_code=201, response_model=UserDTO)
    def patch_user(self, search_data: UserPatchDTO, patch_data: UserPatchDTO):
        response = user_service.patch(self.db, search_data, patch_data)
        return response

    @router.patch(ApiSpec.USERS_INACTIVE, status_code=201, response_model=UserDTO)
    def set_user_inactive(self, search_data: UserPatchDTO, patch_data: UserDeactivateDTO):
        response = user_service.patch_inactive(self.db, search_data, patch_data)
        return response

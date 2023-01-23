from typing import List

from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from fastapi_utils.cbv import cbv

from services import user_service

from db.models import *
from db.dto import *
from db.enums import *
from .api_spec import ApiSpec

from db.database import SessionLocal, engine


router = APIRouter(tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@cbv(router)
class UserView:
    db: Session = Depends(get_db)

    @router.post(ApiSpec.USERS, status_code=HTTPStatus.CREATED)
    def create_user(self, input_data: UserCreateDTO):
        response = user_service.create(self.db, input_data)
        if response != None:
            return Response(status_code=HTTPStatus.CREATED)
        else:
            raise HTTPException(status_code=400, detail="The user was not registered.")

    @router.get(ApiSpec.USERS_DETAILES, status_code=HTTPStatus.OK, response_model=UserProfileDTO)
    def get_user_profile(self, user_id):
        response = user_service.get_profile(self.db, user_id)
        return response

    @router.patch(ApiSpec.USERS_DETAILES, status_code=HTTPStatus.OK, response_model=UserDTO)
    def update_user(self, user_id, input_data: UserPatchDTO):
        response = user_service.patch(self.db, user_id, input_data)
        return response

    @router.patch(ApiSpec.USERS_PASSWORD, status_code=HTTPStatus.NO_CONTENT)
    def change_password(self, user_id, input_data: UserChangePasswordDTO):
        response = user_service.change_password(self.db, user_id, input_data)
        return Response(status_code=HTTPStatus.NO_CONTENT)

    @router.patch(ApiSpec.USERS_BLOCK, status_code=HTTPStatus.NO_CONTENT)
    def block_unblock_user(self, user_id, input_data: UserBlockedDTO):
        response = user_service.block_unblock(self.db, user_id, input_data)
        return Response(status_code=HTTPStatus.NO_CONTENT)

    @router.delete(ApiSpec.USERS_DETAILES, status_code=HTTPStatus.NO_CONTENT)
    def delete_user(self, user_id):
        response = user_service.delete(self.db, user_id)
        return Response(status_code=HTTPStatus.NO_CONTENT)

    # @router.get(ApiSpec.USERS, status_code=200, response_model=List[UserDTO])
    # def get_users(self, skip: int = 0, limit: int = 100):
    #     response = user_service.get_all(self.db, skip=skip, limit=limit)
    #     return response

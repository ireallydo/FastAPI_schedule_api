from typing import List
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from fastapi_utils.cbv import cbv

from services import room_service

from db.models import *
from db.dto import *
from db.enums import *
from .api_spec import ApiSpec

from db.database import SessionLocal, engine


router = APIRouter(tags=["rooms"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@cbv(router)
class RoomView:
    db: Session = Depends(get_db)

    @router.post(ApiSpec.ROOMS, status_code=HTTPStatus.CREATED, response_model=RoomDTO)
    def create_room(self, input_data: RoomCreateDTO):
        response = room_service.create_room(self.db, input_data)
        return response

    @router.get(ApiSpec.ROOMS, status_code=HTTPStatus.OK, response_model=List[RoomDTO])
    def get_all_rooms(self, skip: int = 0, limit=None):
        response = room_service.get_all(self.db, skip, limit)
        return response

    @router.get(ApiSpec.ROOMS_DETAILS, status_code=HTTPStatus.OK, response_model=RoomDTO)
    def get_room_by_number(self, room_number: int):
        response = room_service.get_by_number(self.db, room_number)
        return response

    @router.patch(ApiSpec.ROOMS_DETAILS, status_code=HTTPStatus.OK, response_model=RoomDTO)
    def patch_room(self, room_number: int, input_data: RoomPatchDTO):
        response = room_service.patch(self.db, room_number, input_data)
        return response

    @router.delete(ApiSpec.ROOMS_DETAILS, status_code=HTTPStatus.NO_CONTENT)
    def delete_room(self, room_number: int):
        room_service.delete(self.db, room_number)
        return Response(status_code=HTTPStatus.NO_CONTENT)

    @router.post(ApiSpec.ROOMS_BUSY, status_code=HTTPStatus.OK, response_model=RoomBusyResponseDTO)
    def set_room_busy(self, room_number: int, input_data: RoomBusyRequestDTO):
        print(input_data)
        response = room_service.set_room_busy(self.db, room_number, input_data)
        return response

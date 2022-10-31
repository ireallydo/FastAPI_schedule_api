from typing import List

from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from fastapi import APIRouter
from fastapi_utils.cbv import cbv

from services import room_service

from db.models import *
from db.dto import *
from db.enums import *
from .api_spec import ApiSpec

from db.database import SessionLocal, engine


router = APIRouter(tags=["room"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@cbv(router)
class RoomView:
    db: Session = Depends(get_db)

    @router.post(ApiSpec.ROOMS, status_code=201, response_model=RoomDTO)
    def post_room(self, input_data: RoomCreateDTO):
        response = room_service.create(self.db, input_data)
        return response

    @router.get(ApiSpec.ROOMS, status_code=200, response_model=List[RoomDTO])
    def get_rooms(self, skip: int = 0, limit: int = 100):
        response = room_service.get_all(self.db, skip=skip, limit=limit)
        return response

    @router.get(ApiSpec.GET_ROOM_CLASSTYPE_BY_NUMBER, status_code=200, response_model=RoomDTO)
    def get_room_class_type(self, room_number: int):
        response = room_service.get_room_by_number(self.db, room_number)
        return response

    @router.patch(ApiSpec.ROOMS, status_code=201, response_model=RoomDTO)
    def patch_room(self, search_data: RoomCreateDTO, patch_data: RoomPatchDTO):
        response = room_service.patch(self.db, search_data, patch_data)
        return response

    @router.delete(ApiSpec.ROOMS, responses={200: {'model': str}})
    def delete_room(self, input_data: RoomDeleteDTO):
        room_service.delete(self.db, input_data)
        return JSONResponse(status_code=200, content={'message': f'Кабинет {input_data.room_number} был успешно удален из базы данных!'})

    @router.post(ApiSpec.ROOM_BUSY, status_code=201, response_model=RoomBusyResponseDTO)
    def post_room_busy(self, input_data: RoomBusyRequestDTO):
        room_number=input_data.room_number
        room=room_service.get_room_by_number(self.db, room_number)
        weekday=input_data.weekday
        lesson=input_data.lesson
        room_busy_db_entry = room_service.check_room_busy(self.db, room.id, weekday, lesson)
        if room_busy_db_entry:
            busy_flag=room_busy_db_entry.is_busy
            if busy_flag:
                raise HTTPException(status_code=400, detail=f'''Кабинет уже занят!''')
            else:
                response = room_service.set_room_busy(self.db, room.id, weekday, lesson)
        else:
            response = room_service.create_room_busy(self.db, room.id, weekday, lesson)
        return response

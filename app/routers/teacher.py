from typing import List

from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from fastapi import APIRouter
from fastapi_utils.cbv import cbv

from services import teacher_service

from db.models import *
from db.dto import *
from db.enums import *
from .api_spec import ApiSpec

from db.database import SessionLocal, engine


router = APIRouter(tags=["teacher"])

def get_db():
    db = SessionLocal();
    try:
        yield db;
    finally:
        db.close();

@cbv(router)
class TeacherView:
    db: Session = Depends(get_db)

    @router.post(ApiSpec.TEACHERS, status_code=201, response_model=TeacherDTO)
    def post_teacher(self, input_data: TeacherCreateDTO):
        response = teacher_service.create(self.db, input_data)
        return response

    @router.get(ApiSpec.TEACHERS, status_code=200, response_model=List[TeacherDTO])
    def get_teachers(self, skip: int = 0, limit: int = 100):
        response = teacher_service.get_all(self.db, skip=skip, limit=limit)
        return response

    @router.patch(ApiSpec.TEACHERS, status_code=201, response_model=TeacherDTO)
    def patch_teacher(self, search_data: TeacherCreateDTO, patch_data: TeacherPatchDTO):
        response = teacher_service.patch(self.db, search_data, patch_data)
        return response

    @router.delete(ApiSpec.TEACHERS, responses={200: {'model': str}})
    def delete_teacher(self, input_data: TeacherDeleteDTO):
        teacher_service.delete(self.db, input_data)
        if input_data.second_name:
            middle_name=input_data.second_name
        else:
            middle_name=""
        return JSONResponse(status_code=200, content={'message': f'Преподаватель {input_data.first_name} {middle_name} {input_data.last_name} был успешно удален из базы данных!'})

    @router.post(ApiSpec.TEACHER_BUSY, status_code=201, response_model=TeacherBusyDTO)
    def post_teacher_busy(self, input_data: TeacherBusyDTO):
        teacher_data={"first_name":input_data.first_name, "second_name":input_data.second_name, "last_name":input_data.last_name}
        teacher=teacher_service.get_teacher_by(self.db, teacher_data)
        weekday=input_data.weekday
        lesson=input_data.lesson
        teacher_busy_db_entry = teacher_service.check_teacher_busy(self.db, teacher.id, weekday, lesson)
        print(teacher_busy_db_entry)
        if teacher_busy_db_entry:
            busy_flag=teacher_busy_db_entry.is_busy
            if busy_flag:
                raise HTTPException(status_code=400, detail=f'''Преподаватель уже занят!''')
            else:
                response = teacher_service.set_teacher_busy(self.db, teacher.id, weekday, lesson)
        else:
            response = teacher_service.create_teacher_busy(self.db, teacher.id, weekday, lesson)
        return response

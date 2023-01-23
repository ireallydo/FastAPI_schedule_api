from typing import List
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from fastapi_utils.cbv import cbv

from services import teacher_service

from db.models import *
from db.dto import *
from db.enums import *
from .api_spec import ApiSpec

from db.database import SessionLocal, engine


router = APIRouter(tags=["teachers"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@cbv(router)
class TeacherView:
    db: Session = Depends(get_db)

    @router.post(ApiSpec.TEACHERS, status_code=HTTPStatus.CREATED, response_model=List[TeacherDTO])
    def post_teacher(self, input_data: List[TeacherCreateDTO]):
        response = teacher_service.create(self.db, input_data)
        return response

    @router.get(ApiSpec.TEACHERS, status_code=HTTPStatus.OK, response_model=List[TeacherDTO])
    def get_teachers(self, skip: int=0, limit=None):
        response = teacher_service.get_all(self.db, skip, limit)
        return response

    @router.get(ApiSpec.TEACHERS_DETAIL, status_code=HTTPStatus.OK, response_model=TeacherProfileDTO)
    def get_teacher_profile(self, user_id):
        response = teacher_service.get_profile(self.db, user_id)
        return response

    @router.delete(ApiSpec.TEACHERS_DETAIL, status_code=HTTPStatus.NO_CONTENT)
    def delete_teacher(self, user_id):
        teacher_service.delete(self.db, user_id)
        return Response(status_code=HTTPStatus.NO_CONTENT)


    @router.post(ApiSpec.TEACHERS_BUSY, status_code=HTTPStatus.OK, response_model=TeacherBusyResponseDTO)
    def set_teacher_busy(self, user_id, input_data: TeacherBusyRequestDTO):
        response = teacher_service.set_teacher_busy(self.db, user_id, input_data)
        return response


    @router.post(ApiSpec.TEACHERS_MODULES, status_code=HTTPStatus.OK, response_model=TeachersToModulesDTO)
    def create_teachers_modules(self, user_id, input_data: TeachersToModulesCreateDTO):
        response = teacher_service.create_modules(self.db, user_id, input_data)
        return response

    @router.get(ApiSpec.TEACHERS_MODULES, status_code=HTTPStatus.OK, response_model=TeachersToModulesDTO)
    def get_teachers_modules(self, user_id):
        response = teacher_to_module_service.get_modules(self.db, user_id)
        return response

    @router.delete(ApiSpec.TEACHERS_MODULES, status_code=HTTPStatus.NO_CONTENT)
    def delete_teachers_modules(self, user_id, input_data: TeachersToModulesDeleteDTO):
        teacher_to_module_service.delete_association(self.db, user_id, input_data)
        return Response(status_code=HTTPStatus.NO_CONTENT)

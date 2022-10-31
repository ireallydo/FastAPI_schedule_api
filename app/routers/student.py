from typing import List, Union

from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from fastapi import APIRouter
from fastapi_utils.cbv import cbv

from services import student_service

from db.models import *
from db.dto import *
from db.enums import *
from .api_spec import ApiSpec

from db.database import SessionLocal, engine


router = APIRouter(tags=["student"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@cbv(router)
class StudentView:
    db: Session = Depends(get_db)

    @router.post(ApiSpec.STUDENTS, status_code=201, response_model=StudentDTO)
    def post_student(self, input_data: StudentCreateDTO):
        response = student_service.create(self.db, input_data)
        return response

    @router.get(ApiSpec.STUDENTS, status_code=200, response_model=List[StudentDTO])
    def get_students(self, skip: int = 0, limit: int = 100):
        response = student_service.get_all(self.db, skip=skip, limit=limit)
        return response

    @router.get(ApiSpec.GET_STUDENT_BY_NAME, status_code=200, response_model=StudentDTO)
    def get_student_by_name(self, first_name: str, last_name: str, second_name: Union[str, None]=None):
        response = student_service.get_by_name(self.db, first_name, second_name, last_name)
        return response

    @router.get(ApiSpec.GET_STUDENTS_BY_GROUP, status_code=200, response_model=List[StudentDTO])
    def get_students_by_group(self, group_number: AcademicGroupsEnum, skip: int = 0, limit: int = 100):
        response = student_service.get_by_group(self.db, group_number, skip=skip, limit=limit)
        return response

    @router.get(ApiSpec.GET_STUDENTS_BY_YEAR, status_code=200, response_model=List[StudentDTO])
    def get_students_by_year(self, year_number: AcademicYearsEnum, skip: int = 0, limit: int = 100):
        print(year_number)
        response = student_service.get_by_year(self.db, year_number, skip=skip, limit=limit)
        return response

    @router.patch(ApiSpec.STUDENTS, status_code=201, response_model=StudentDTO)
    def patch_student(self, search_data: StudentPatchDTO, patch_data: StudentPatchDTO):
        response = student_service.patch(self.db, search_data, patch_data)
        return response

    @router.delete(ApiSpec.STUDENTS, responses={200: {'model': str}})
    def delete_student(self, input_data: StudentDeleteDTO):
        student_service.delete(self.db, input_data)
        if input_data.second_name:
            second_name=input_data.second_name
        else:
            second_name=""
        return JSONResponse(status_code=200, content={'message': f'Студент {input_data.first_name} {second_name} {input_data.last_name} из группы {input_data.academic_group}, {input_data.academic_year} год обучения, был успешно удален из базы данных!'})

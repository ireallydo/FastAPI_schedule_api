from typing import List, Union

from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from fastapi_utils.cbv import cbv

from services import student_service

from db.models import *
from db.dto import *
from db.enums import *
from .api_spec import ApiSpec

from db.database import SessionLocal, engine


router = APIRouter(tags=["students"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@cbv(router)
class StudentView:
    db: Session = Depends(get_db)

    @router.post(ApiSpec.STUDENTS, status_code=HTTPStatus.CREATED, response_model=List[StudentDTO])
    def create_students(self, input_data: List[StudentCreateDTO]):
        response = student_service.create(self.db, input_data)
        return response

    @router.get(ApiSpec.STUDENTS_DETAIL, status_code=HTTPStatus.OK, response_model=StudentProfileDTO)
    def get_student_profile(self, user_id):
        response = student_service.get_by_id(self.db, user_id)
        pass

    @router.get(ApiSpec.STUDENTS_BY_GROUP, status_code=HTTPStatus.OK, response_model=List[StudentDTO])
    def get_students_by_group(self, group_number: AcademicGroupsEnum, skip: int = 0, limit: int = 100):
        response = student_service.get_by_group(self.db, group_number, skip=skip, limit=limit)
        return response

    @router.get(ApiSpec.STUDENTS_BY_YEAR, status_code=HTTPStatus.OK, response_model=List[StudentDTO])
    def get_students_by_year(self, year_number: AcademicYearsEnum, skip: int = 0, limit: int = 100):
        print(year_number)
        response = student_service.get_by_year(self.db, year_number, skip=skip, limit=limit)
        return response

    @router.patch(ApiSpec.STUDENTS_DETAIL, status_code=HTTPStatus.OK, response_model=StudentDTO)
    def update_student(self, user_id, input_data: StudentPatchDTO):
        response = student_service.patch(self.db, user_id, input_data)
        return response

    @router.delete(ApiSpec.STUDENTS_DETAIL, status_code=HTTPStatus.NO_CONTENT)
    def delete_student(self, user_id):
        student_service.delete(self.db, user_id)
        return Response(status_code=HTTPStatus.NO_CONTENT)


    # @router.get(ApiSpec.GET_STUDENT_BY_NAME, status_code=200, response_model=StudentDTO)
    # def get_student_by_name(self, first_name: str, last_name: str, second_name: Union[str, None]=None):
    #     response = student_service.get_by_name(self.db, first_name, second_name, last_name)
    #     return response

from typing import List
from http import HTTPStatus
from fastapi import APIRouter, Response
from fastapi_utils.cbv import cbv
from services.student_service import student_service
from db.dto import CreateStudentsResp, StudentCreateDTO, StudentProfileDTO,\
    StudentDTO, StudentPatchDTO
from db.enums import AcademicGroupsEnum, AcademicYearsEnum
from .api_spec import ApiSpec
from mixins import AuthMixin
from utils import available_roles
from db.enums import UserRolesEnum as Roles


router = APIRouter(tags=["students"])


@cbv(router)
class StudentView(AuthMixin):

    @router.post(ApiSpec.STUDENTS, status_code=HTTPStatus.OK, response_model=CreateStudentsResp)
    @available_roles(role=Roles.ADMIN)
    async def create_students(self, input_data: List[StudentCreateDTO]):
        response = await student_service.create(input_data)
        return response

    @router.get(ApiSpec.STUDENTS_DETAILS, status_code=HTTPStatus.OK, response_model=StudentProfileDTO)
    @available_roles(role=Roles.ADMIN, self_action=True)
    async def get_student_profile(self, user_id: str):
        """returns full information about the student by id, including registration token"""
        response = await student_service.get_by_id(user_id)
        return response

    @router.get(ApiSpec.STUDENTS_BY_GROUP, status_code=HTTPStatus.OK, response_model=List[StudentDTO])
    @available_roles(role=Roles.ADMIN)
    async def get_students_by_group(self, group_number: AcademicGroupsEnum, skip: int = 0, limit: int = None):
        """return active (not deleted) students by group"""
        response = await student_service.get_all_by(skip, limit, academic_group=group_number)
        return response

    @router.get(ApiSpec.STUDENTS_BY_YEAR, status_code=HTTPStatus.OK, response_model=List[StudentDTO])
    @available_roles(role=Roles.ADMIN)
    async def get_students_by_year(self, year_number: AcademicYearsEnum, skip: int = 0, limit: int = None):
        """return active (not deleted) students by year"""
        response = await student_service.get_all_by(skip, limit, academic_year=year_number)
        return response

    @router.patch(ApiSpec.STUDENTS_DETAILS, status_code=HTTPStatus.OK, response_model=StudentDTO)
    @available_roles(role=Roles.ADMIN)
    async def update_student(self, user_id: str, input_data: StudentPatchDTO):
        """update student group and/or year"""
        response = await student_service.patch(user_id, input_data)
        return response

    @router.delete(ApiSpec.STUDENTS_DETAILS, status_code=HTTPStatus.NO_CONTENT)
    @available_roles(role=Roles.ADMIN)
    async def delete_student(self, user_id: str):
        """updates student's deleted_at field with the current time stamp"""
        await student_service.delete(user_id)
        return Response(status_code=HTTPStatus.NO_CONTENT)

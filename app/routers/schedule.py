from typing import List
from http import HTTPStatus
from fastapi import HTTPException, APIRouter, Response
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv

from services.schedule_service import schedule_service
# group_service, module_service, teacher_service

from db.dto import *
from .api_spec import ApiSpec
from mixins import AuthMixin
from utils import available_roles
from db.enums import UserRolesEnum as Roles
from db.enums import SemestersEnum


router = APIRouter(tags=["schedule"])


@cbv(router)
class ScheduleView(AuthMixin):

    @router.post(ApiSpec.SCHEDULE_AUTO, status_code=HTTPStatus.OK, response_model=ScheduleOutDTO)
    @available_roles(role=Roles.ADMIN)
    async def create_schedule_auto(self, input_data: ScheduleCreateDTO):
        """automatic creation of schedule:
        group is checked for being busy
        teacher and room are assigned automatically"""
        response = await schedule_service.create_auto(input_data)
        return response

    @router.post(ApiSpec.SCHEDULE_MANUAL, status_code=HTTPStatus.OK, response_model=ScheduleOutDTO)
    @available_roles(role=Roles.ADMIN)
    async def create_schedule_manually(self, input_data: ScheduleCreateManuallyDTO):
        """requires manual input of all data, does not support auto-generation for fields
        checks busy rooms, teachers and groups"""
        response = await schedule_service.create_manually(input_data)
        return response

    @router.get(ApiSpec.SCHEDULE_GROUP, status_code=HTTPStatus.OK, response_model=GroupScheduleDTO)
    @available_roles(role=Roles.STUDENT)
    async def get_schedule_by_group(self, semester: SemestersEnum, group_number: AcademicGroupsEnum,
                                    skip: int = 0, limit: int = None):
        response = await schedule_service.get_by_group(skip, limit, semester=semester, group_number=group_number)
        return response

    @router.get(ApiSpec.SCHEDULE_TEACHER, status_code=HTTPStatus.OK, response_model=TeacherScheduleDTO)
    @available_roles(role=Roles.STUDENT)
    async def get_schedule_by_teacher(self, semester: SemestersEnum, teacher_id: str,
                                      skip: int = 0, limit: int = None):
        response = await schedule_service.get_by_teacher(skip, limit, semester=semester, teacher_id=teacher_id)
        return response

    @router.delete(ApiSpec.DELETE_SCHEDULE, status_code=HTTPStatus.NO_CONTENT)
    @available_roles(role=Roles.ADMIN)
    async def delete_schedule(self, schedule_id: str):
        """delete schedule entry by id"""
        await schedule_service.delete_schedule_entry(schedule_id)
        return Response(status_code=HTTPStatus.NO_CONTENT)

    @router.delete(ApiSpec.CLEAR_SCHEDULE, status_code=HTTPStatus.NO_CONTENT)
    @available_roles(role=Roles.ADMIN)
    async def clear_schedule(self, semester: SemestersEnum):
        """clear semester schedule for all groups and teachers"""
        await schedule_service.clear_semester_schedule(semester)
        return Response(status_code=HTTPStatus.NO_CONTENT)

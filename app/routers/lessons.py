from typing import List
from http import HTTPStatus
from fastapi import APIRouter, Response
from fastapi_utils.cbv import cbv
from services.lesson_service import lesson_service
from db.models import *
from db.dto import LessonDTO, LessonCreateDTO, LessonPatchDTO
from db.enums import LessonsEnum
from .api_spec import ApiSpec
from mixins import AuthMixin
from utils import available_roles
from db.enums import UserRolesEnum as Roles


router = APIRouter(tags=["lessons"])


@cbv(router)
class LessonView(AuthMixin):

    @router.post(ApiSpec.LESSONS, status_code=HTTPStatus.CREATED, response_model=LessonDTO)
    @available_roles(role=Roles.ADMIN)
    async def create_lesson(self, input_data: LessonCreateDTO):
        response = await lesson_service.create_lesson(input_data)
        return response

    @router.get(ApiSpec.LESSONS, status_code=HTTPStatus.OK, response_model=List[LessonDTO])
    @available_roles(role=Roles.ADMIN)
    async def get_all_lessons(self, skip: int = 0, limit=None):
        response = await lesson_service.get_all(skip, limit)
        return response

    @router.get(ApiSpec.LESSONS_DETAILS, status_code=HTTPStatus.OK, response_model=LessonDTO)
    @available_roles(role=Roles.ADMIN)
    async def get_lesson_by_number(self, lesson_number: LessonsEnum):
        response = await lesson_service.get_by_number(lesson_number)
        return response

    @router.patch(ApiSpec.LESSONS_DETAILS, status_code=HTTPStatus.OK, response_model=LessonDTO)
    @available_roles(role=Roles.ADMIN)
    async def patch_lesson(self, lesson_number: LessonsEnum, input_data: LessonPatchDTO):
        response = await lesson_service.patch(lesson_number, input_data)
        return response

    @router.delete(ApiSpec.LESSONS_DETAILS, status_code=HTTPStatus.NO_CONTENT)
    @available_roles(role=Roles.ADMIN)
    async def delete_lesson(self, lesson_number: LessonsEnum):
        await lesson_service.delete(lesson_number)
        return Response(status_code=HTTPStatus.NO_CONTENT)

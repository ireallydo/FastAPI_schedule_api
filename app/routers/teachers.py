from typing import List
from http import HTTPStatus
from fastapi import APIRouter, Response
from fastapi_utils.cbv import cbv
from services.teacher_service import teacher_service
from services.module_service import module_service
from db.dto import CreateTeachersResponse, TeacherCreateDTO, TeacherDTO,\
    TeacherProfileDTO, TeacherBusyResponseDTO, TeacherBusyRequestDTO,\
    TeacherWithModulesDTO, TeacherCreateModulesDTO, TeacherDeleteModuleDTO, TeacherModulesDTO
from .api_spec import ApiSpec
from mixins import AuthMixin
from utils import available_roles
from db.enums import UserRolesEnum as Roles


router = APIRouter(tags=["teachers"])


@cbv(router)
class TeacherView(AuthMixin):

    @router.post(ApiSpec.TEACHERS, status_code=HTTPStatus.CREATED, response_model=CreateTeachersResponse)
    @available_roles(role=Roles.ADMIN)
    async def create_teachers(self, input_data: List[TeacherCreateDTO]):
        response = await teacher_service.create(input_data)
        return response

    @router.get(ApiSpec.TEACHERS, status_code=HTTPStatus.OK, response_model=List[TeacherDTO])
    @available_roles(role=Roles.ADMIN)
    async def get_all_teachers(self, skip: int = 0, limit: int = None):
        """get all active (deleted_at is None) teachers"""
        response = await teacher_service.get_all(skip, limit)
        return response

    @router.get(ApiSpec.TEACHERS_DETAILS, status_code=HTTPStatus.OK, response_model=TeacherProfileDTO)
    @available_roles(role=Roles.ADMIN, self_action=True)
    async def get_teacher_profile(self, user_id: str):
        """returns full information about the teacher by id, including registration token"""
        response = await teacher_service.get_by_id(user_id)
        return response

    @router.delete(ApiSpec.TEACHERS_DETAILS, status_code=HTTPStatus.NO_CONTENT)
    @available_roles(role=Roles.ADMIN)
    async def delete_teacher(self, user_id: str):
        """updates teacher's deleted_at field with the current time stamp"""
        await teacher_service.delete(user_id)
        return Response(status_code=HTTPStatus.NO_CONTENT)

    @router.post(ApiSpec.TEACHERS_MODULES, status_code=HTTPStatus.OK, response_model=TeacherWithModulesDTO)
    @available_roles(role=Roles.ADMIN)
    async def create_teachers_modules(self, user_id: str, input_data: TeacherCreateModulesDTO):
        modules = [await module_service.get_by_id(module_id) for module_id in input_data.modules_id]
        response = await teacher_service.create_teacher_modules(user_id, modules)
        return response

    @router.get(ApiSpec.TEACHERS_MODULES, status_code=HTTPStatus.OK, response_model=List[TeacherModulesDTO])
    @available_roles(role=Roles.ADMIN, self_action=True)
    async def get_teachers_modules(self, user_id: str):
        response = await teacher_service.get_modules(user_id)
        return response

    @router.delete(ApiSpec.TEACHERS_MODULES, status_code=HTTPStatus.NO_CONTENT)
    @available_roles(role=Roles.ADMIN)
    async def delete_teachers_module(self, user_id: str, input_data: TeacherDeleteModuleDTO):
        module = await module_service.get_by_id(input_data.module_id)
        await teacher_service.delete_teacher_module(user_id, module)
        return Response(status_code=HTTPStatus.NO_CONTENT)

    @router.post(ApiSpec.TEACHERS_BUSY, status_code=HTTPStatus.OK, response_model=TeacherBusyResponseDTO)
    @available_roles(role=Roles.ADMIN)
    async def set_teacher_busy(self, user_id, input_data: TeacherBusyRequestDTO):
        response = await teacher_service.set_teacher_busy(user_id, input_data)
        return response

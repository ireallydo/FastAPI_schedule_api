from typing import List
from http import HTTPStatus
from fastapi import APIRouter, Response
from fastapi_utils.cbv import cbv
from services.module_service import module_service
from db.dto import ModuleDTO, ModuleCreateDTO, ModuleTeachersDTO
from .api_spec import ApiSpec
from mixins import AuthMixin
from utils import available_roles
from db.enums import UserRolesEnum as Roles


router = APIRouter(tags=["modules"])


@cbv(router)
class ModuleView(AuthMixin):

    @router.post(ApiSpec.MODULES, status_code=HTTPStatus.CREATED, response_model=ModuleDTO)
    @available_roles(role=Roles.ADMIN)
    async def create_module(self, input_data: ModuleCreateDTO):
        response = await module_service.create_module(input_data)
        return response

    @router.get(ApiSpec.MODULES, status_code=HTTPStatus.OK, response_model=List[ModuleDTO])
    @available_roles(role=Roles.ADMIN)
    async def get_all_modules(self, skip: int = 0, limit=None):
        response = await module_service.get_all_modules(skip, limit)
        return response

    @router.get(ApiSpec.MODULES_DETAILS, status_code=HTTPStatus.OK, response_model=ModuleDTO)
    @available_roles(role=Roles.ADMIN)
    async def get_module_by_id(self, module_id: str):
        response = await module_service.get_by_id(module_id)
        return response

    @router.get(ApiSpec.MODULES_TEACHERS, status_code=HTTPStatus.OK, response_model=ModuleTeachersDTO)
    @available_roles(role=Roles.ADMIN)
    async def get_module_teachers(self, module_id: str):
        response = await module_service.get_teachers(module_id)
        return response

    @router.delete(ApiSpec.MODULES_DETAILS, status_code=HTTPStatus.NO_CONTENT)
    @available_roles(role=Roles.ADMIN)
    async def delete_module(self, module_id: str):
        await module_service.delete(module_id)
        return Response(status_code=HTTPStatus.NO_CONTENT)

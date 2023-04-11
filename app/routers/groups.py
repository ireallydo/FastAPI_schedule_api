from fastapi import APIRouter
from fastapi_utils.cbv import cbv
from db.enums import AcademicGroupsEnum
from services.group_service import group_service
from db.dto import GroupBusyResponseDTO, GroupBusyRequestDTO
from .api_spec import ApiSpec
from mixins import AuthMixin
from utils import available_roles
from db.enums import UserRolesEnum as Roles


router = APIRouter(tags=["groups"])


@cbv(router)
class GroupBusyView(AuthMixin):

    @router.post(ApiSpec.GROUP_BUSY, status_code=201, response_model=GroupBusyResponseDTO)
    @available_roles(role=Roles.ADMIN)
    async def set_group_busy(self, group_number: AcademicGroupsEnum, input_data: GroupBusyRequestDTO):
        response = await group_service.set_group_busy(group_number, input_data)
        return response

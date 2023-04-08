from http import HTTPStatus
from fastapi import APIRouter, Response
from fastapi_utils.cbv import cbv
from services.user_service import user_service
from db.dto import UserProfileDTO, UserDTO,\
    UserPatchDTO, UserChangePasswordDTO, UserBlockedDTO
from .api_spec import ApiSpec
from mixins import AuthMixin
from utils import available_roles
from db.enums import UserRolesEnum as Roles


router = APIRouter(tags=["users"])


@cbv(router)
class UserView(AuthMixin):

    @router.get(ApiSpec.USERS_DETAILS, status_code=HTTPStatus.OK, response_model=UserProfileDTO)
    @available_roles(role=Roles.ADMIN, self_action=True)
    async def get_user_profile(self, user_id: str):
        response = await user_service.get_profile(user_id)
        return response

    @router.patch(ApiSpec.USERS_DETAILS, status_code=HTTPStatus.OK, response_model=UserDTO)
    @available_roles(role=Roles.STUDENT, self_action=True)
    async def update_user(self, user_id: str, input_data: UserPatchDTO):
        response = await user_service.patch(user_id, input_data)
        return response

    @router.patch(ApiSpec.USERS_PASSWORD, status_code=HTTPStatus.NO_CONTENT)
    @available_roles(role=Roles.STUDENT, self_action=True)
    async def change_password(self, user_id: str, input_data: UserChangePasswordDTO):
        """changes user password but does not break the current session"""
        await user_service.change_password(user_id, input_data)
        return Response(status_code=HTTPStatus.NO_CONTENT)

    @router.patch(ApiSpec.USERS_BLOCK, status_code=HTTPStatus.NO_CONTENT)
    @available_roles(role=Roles.ADMIN)
    async def block_unblock_user(self, user_id: str, input_data: UserBlockedDTO):
        await user_service.patch(user_id, input_data)
        return Response(status_code=HTTPStatus.NO_CONTENT)

    @router.delete(ApiSpec.USERS_DETAILS, status_code=HTTPStatus.NO_CONTENT)
    @available_roles(role=Roles.ADMIN, self_action=True)
    async def delete_user(self, user_id: str):
        await user_service.delete_user(user_id)
        return Response(status_code=HTTPStatus.NO_CONTENT)

    @router.patch(ApiSpec.USERS_RESTORE, status_code=HTTPStatus.NO_CONTENT)
    @available_roles(role=Roles.ADMIN)
    async def restore_user(self, user_id: str):
        """sets 'deleted' user is_active field to True"""
        await user_service.restore_user(user_id)
        return Response(status_code=HTTPStatus.NO_CONTENT)

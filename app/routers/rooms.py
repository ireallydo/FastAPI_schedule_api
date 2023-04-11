from typing import List
from http import HTTPStatus
from fastapi import APIRouter, Response
from fastapi_utils.cbv import cbv
from services.room_service import room_service
from db.dto import RoomCreateDTO, RoomDTO, RoomPatchDTO,\
    RoomBusyRequestDTO, RoomBusyResponseDTO
from .api_spec import ApiSpec
from mixins import AuthMixin
from utils import available_roles
from db.enums import UserRolesEnum as Roles


router = APIRouter(tags=["rooms"])


@cbv(router)
class RoomView(AuthMixin):

    @router.post(ApiSpec.ROOMS, status_code=HTTPStatus.CREATED, response_model=RoomDTO)
    @available_roles(role=Roles.ADMIN)
    async def create_room(self, input_data: RoomCreateDTO):
        response = await room_service.create_room(input_data)
        return response

    @router.get(ApiSpec.ROOMS, status_code=HTTPStatus.OK, response_model=List[RoomDTO])
    @available_roles(role=Roles.ADMIN)
    async def get_all_rooms(self, skip: int = 0, limit=None):
        response = await room_service.get_all(skip, limit)
        return response

    @router.get(ApiSpec.ROOMS_DETAILS, status_code=HTTPStatus.OK, response_model=RoomDTO)
    @available_roles(role=Roles.ADMIN)
    async def get_room_by_number(self, room_number: int):
        response = await room_service.get_by_number(room_number)
        return response

    @router.patch(ApiSpec.ROOMS_DETAILS, status_code=HTTPStatus.OK, response_model=RoomDTO)
    @available_roles(role=Roles.ADMIN)
    async def patch_room(self, room_number: int, input_data: RoomPatchDTO):
        response = await room_service.patch(room_number, input_data)
        return response

    @router.delete(ApiSpec.ROOMS_DETAILS, status_code=HTTPStatus.NO_CONTENT)
    @available_roles(role=Roles.ADMIN)
    async def delete_room(self, room_number: int):
        await room_service.delete(room_number)
        return Response(status_code=HTTPStatus.NO_CONTENT)

    @router.post(ApiSpec.ROOMS_BUSY, status_code=HTTPStatus.OK, response_model=RoomBusyResponseDTO)
    @available_roles(role=Roles.ADMIN)
    async def set_room_busy(self, room_number: int, input_data: RoomBusyRequestDTO):
        response = await room_service.set_room_busy(room_number, input_data)
        return response

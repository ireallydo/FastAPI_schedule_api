from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Response
from fastapi_utils.cbv import cbv
from services.user_service import user_service
from db.dto import UserRegisterDTO
from .api_spec import ApiSpec


router = APIRouter(tags=["registration"])


@cbv(router)
class RegistrationView:
    @router.post(ApiSpec.REGISTRATION, status_code=HTTPStatus.CREATED)
    async def create_user(self, input_data: UserRegisterDTO):
        response = await user_service.create(input_data)
        if response is None:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail="The user was not registered. Please contact administration.")
        else:
            return Response(status_code=HTTPStatus.CREATED)

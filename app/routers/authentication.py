from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_utils.cbv import cbv
from services.auth_service import auth_service
from db.models import *
from db.dto import LoginRespDTO
from .api_spec import ApiSpec


router = APIRouter(tags=["authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")


@cbv(router)
class AuthView:

    @router.post(ApiSpec.AUTH, status_code=200, response_model=LoginRespDTO)
    async def login(self, form_data: OAuth2PasswordRequestForm = Depends()):
        resp = await auth_service.login_user(form_data)
        return resp

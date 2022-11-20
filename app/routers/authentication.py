from sorcery import dict_of
from jose import jwt

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi_utils.cbv import cbv

from sqlalchemy.orm import Session

import utils
from services import auth_service, user_service
from db.models import *
from db.dto import *
from .api_spec import ApiSpec
from db.database import SessionLocal, engine


router = APIRouter(tags=["authentication"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")

@cbv(router)
class AuthView:
    db: Session = Depends(get_db)

    @router.get(ApiSpec.AUTH_USER, status_code=200, response_model=UserDTO)
    def get_current_user(self, token = Depends(oauth2_scheme)):
        user = auth_service.get_current_user(self.db, token)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find user")
        return user

    @router.post(ApiSpec.AUTH, status_code=201)
    def login(self, form_data: OAuth2PasswordRequestForm = Depends()):
        user = user_service.get_by_login(self.db, form_data.username)
        if not user:
            raise HTTPException(status_code=400, detail='Неправильное имя пользователя или пароль')
        if not utils.verify_password(form_data.password, user.password):
            raise HTTPException(status_code=400, detail='Неправильное имя пользователя или пароль')

        access_token = utils.create_access_token(user.email)
        refresh_token = utils.create_refresh_token(user.email)
        user_id = user.id

        return {'access_token': access_token,
                'refresh_token': refresh_token}

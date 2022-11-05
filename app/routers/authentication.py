from typing import List

from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from fastapi import APIRouter
from fastapi_utils.cbv import cbv

from services import auth_service, user_service

from db.models import *
from db.dto import *
from db.enums import *
from .api_spec import ApiSpec

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from db.database import SessionLocal, engine


router = APIRouter(tags=["authentication"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def fake_hash_password(db, password: str):
    return password

db: Session = Depends(get_db)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(db, token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(db, token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Пользователь не авторизован', headers={'WWW-Authenticate': 'Bearer'})
    return user

def fake_decode_token(db, token):
    username = token
    user = user_dao.get_by(db, username)
    return user

def get_current_active_user(current_user: UserDTO = Depends(get_current_user)):
    if current_user.is_active == False:
        raise HTTPException(status_code=400, detail='Пользователь удален')
    return current_user


@cbv(router)
class AuthView:
    db: Session = Depends(get_db)

    @router.get(ApiSpec.AUTH_USER, status_code=200, response_model=UserDTO)
    def get_current_user(current_user: UserDTO = Depends(get_current_active_user)):
        return current_user

    @router.post(ApiSpec.AUTH, status_code=201)
    def login(self, form_data: OAuth2PasswordRequestForm = Depends()):
        user = user_service.get_by_login(self.db, form_data.username)
        if not user:
            raise HTTPException(status_code=400, detail='Неправильное имя пользователя или пароль')
        hashed_password = fake_hash_password(self.db, form_data.password)
        if not hashed_password == user.password:
            raise HTTPException(status_code=400, detail='Неправильное имя пользователя или пароль')
        return {'access_token': user.login, 'token_type': 'bearer'}

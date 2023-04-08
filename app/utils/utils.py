from passlib.context import CryptContext
from settings import Settings
from typing import Union, Any
from datetime import datetime, timedelta
from jose import jwt
from db.dto import *


settings = Settings()


password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


async def get_exp_time(expiration_delta: timedelta, expire_minutes: timedelta) -> datetime:
    if expiration_delta is not None:
        expiration_delta = datetime.utcnow() + expiration_delta
    else:
        expiration_delta = datetime.utcnow() + expire_minutes

    print('EXPIRATION DELTA')
    print(type(expiration_delta))
    print(type(expire_minutes))
    return expiration_delta


async def create_access_token(subject: Union[str, Any], expiration_delta: timedelta = None) -> tuple:
    expiration_delta = await get_exp_time(expiration_delta, settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    encode_info = {"exp": expiration_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(encode_info, settings.JWT_KEY, settings.TOKEN_ALGO)
    return encoded_jwt, expiration_delta


async def create_refresh_token(subject: Union[str, Any], expiration_delta: timedelta = None) -> tuple:
    expiration_delta = await get_exp_time(expiration_delta, settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    encode_info = {"exp": expiration_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(encode_info, settings.JWT_REFRESH_KEY, settings.TOKEN_ALGO)
    return encoded_jwt, expiration_delta

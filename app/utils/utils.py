from passlib.context import CryptContext
from settings import Settings
from typing import Union, Any
from datetime import datetime
# from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from db.dto import *


settings = Settings()


# password hashing and check functions

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)

# jwt tokens functions

def create_access_token(subject: Union[str, Any], expiration_delta: int = None) -> str:
    if expiration_delta is not None:
        expiration_delta = datetime.utcnow() + expiration_delta
    else:
        expiration_delta = datetime.utcnow() + settings.ACCESS_TOKEN_EXPIRE_MINUTES
    encode_info = {"exp": expiration_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(encode_info, settings.JWT_KEY, settings.TOKEN_ALGO)
    return encoded_jwt, expiration_delta


def get_exp_time_access_token(subject: Union[str, Any], expiration_delta: int = None):
    if expiration_delta is not None:
        expiration_delta = datetime.utcnow() + expiration_delta
    else:
        expiration_delta = datetime.utcnow() + settings.ACCESS_TOKEN_EXPIRE_MINUTES
    return expiration_delta


def create_refresh_token(subject: Union[str, Any], expiration_delta: int = None) -> str:
    if expiration_delta is not None:
        expiration_delta = datetime.utcnow() + expiration_delta
    else:
        expiration_delta = datetime.utcnow() + settings.REFRESH_TOKEN_EXPIRE_MINUTES
    encode_info = {"exp": expiration_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(encode_info, settings.JWT_REFRESH_KEY, settings.TOKEN_ALGO)
    return encoded_jwt, expiration_delta


# get current user dependency

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")

# def get_current_user(token: str = Depends(oauth2_scheme)) -> UserDTO:
#     print("utils file")
#     try:
#         payload =jwt.decode(token, settings.JWT_KEY, algorithms=[settings.TOKEN_ALGO])
#         token_data = TokenPayload(**payload)
#         if datetime.fromtimestamp(token_data.exp) < datetime.now():
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired", headers={"WWW-Authenticate": "Bearer"})
#     except(jwt.JWTError, ValidationError):
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
#     user: Union[dict[str, Any], None] = auth_service.get_user_by_token(db, token_data.sub)
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find user")
#     return user

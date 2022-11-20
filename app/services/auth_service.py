from jose import jwt

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from db.models import *
from db.dto import *
from db.dao import user_dao
from services import user_service
from settings import Settings


settings = Settings()

def get_current_user(db, token):
    try:
        payload =jwt.decode(token, settings.JWT_KEY, algorithms=[settings.TOKEN_ALGO])
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired", headers={"WWW-Authenticate": "Bearer"})
    except(jwt.JWTError, ValidationError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    user: Union[dict[str, Any], None] = user_service.get_by_login(db, token_data.sub)
    if user.is_active == False:
        raise HTTPException(status_code=400, detail='Пользователь удален')
    return user

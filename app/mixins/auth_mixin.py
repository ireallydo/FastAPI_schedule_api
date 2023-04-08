from jose import jwt
from fastapi import Depends, Request
from http import HTTPStatus
from fastapi import HTTPException
from loguru import logger
from db.dto import AuthHeadersDTO, TokenPayload
from services.user_service import user_service
from settings import Settings


settings = Settings()


async def get_auth_headers(request: Request) -> AuthHeadersDTO:
    logger.info("AuthMixin: get auth headers from request")
    headers_check = request.headers.items()
    for item in headers_check:
        if item[0] == 'authorization':
            token = item[1].strip().split(" ")[-1]
            break
        elif item == headers_check[-1]:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Did not get credentials.')
    try:
        payload = jwt.decode(token, settings.JWT_KEY, algorithms=[settings.TOKEN_ALGO])
        token_data = TokenPayload(**payload)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                            detail="Unauthorized")
    except jwt.JWTError:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN,
                            detail="Could not validate credentials")
    user = await user_service.get_by_login(token_data.sub)
    if not user.is_active:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail='The user was deleted. Please contact administration.')
    resp = AuthHeadersDTO(
        user_id=user.id,
        role=user.role,
        login=user.login
    )
    return resp


class AuthMixin:
    auth_headers: AuthHeadersDTO = Depends(get_auth_headers)

from typing import Union
from pydantic import BaseModel
from uuid import UUID


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class LoginRespDTO(BaseModel):
    user_id: Union[str, UUID]
    login: str
    role: str
    access_token: str
    refresh_token: str


class AuthHeadersDTO(BaseModel):
    user_id: Union[str, UUID]
    role: str
    login: str

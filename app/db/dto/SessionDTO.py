from typing import Union
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class SessionBaseDTO(BaseModel):
    class Config:
        orm_mode = True


class SessionCreateDTO(SessionBaseDTO):
    user_id: Union[UUID, str]
    login: str
    role: str
    access_expire_time: Union[datetime, str]
    refresh_expire_time: Union[datetime, str]
    access_token: str
    refresh_token: str
    blocked: bool
    is_active: bool


class SessionPatchDTO(SessionBaseDTO):
    pass

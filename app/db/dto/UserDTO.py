from typing import List, Union, Dict, Optional
from pydantic import BaseModel
from datetime import datetime

from uuid import UUID

from db.enums import UserRolesEnum
from db.dto import ModuleDTO


class UserBaseDTO(BaseModel):
    class Config:
        orm_mode = True

class UserCreateDTO(UserBaseDTO):
    role: UserRolesEnum
    login: str
    password: str
    email: str
    registration_token: str
    first_name: str
    second_name: Optional[str]
    last_name: str
    birth_date: Union[str, datetime]

class UserDTO(UserBaseDTO):
    id: UUID
    login: str
    email: str

class UserProfileDTO(UserDTO):
    is_active: bool
    blocked: bool

class UserPatchDTO(UserBaseDTO):
    email: str

class UserChangePasswordDTO(UserBaseDTO):
    password: str

class UserBlockedDTO(UserBaseDTO):
    blocked: bool

class UserDeleteDTO(UserBaseDTO):
    is_active: bool

from typing import List, Union, Dict, Optional
from pydantic import BaseModel

from uuid import UUID

from db.enums import ClassTypesEnum, AcademicYearsEnum, WeekdaysEnum, LessonsEnum
from db.dto import ModuleDTO


class UserBaseDTO(BaseModel):
    class Config:
        orm_mode = True

class UserCreateDTO(UserBaseDTO):
    login: str
    password: str
    email: str

class UserDTO(UserBaseDTO):
    id: UUID
    login: str
    email: str
    is_active: bool

class UserPatchDTO(UserCreateDTO):
    login: str
    password: str

class UserChangePasswordDTO(UserBaseDTO):
    password: str

class UserDeactivateDTO(UserBaseDTO):
    login: str
    is_active: bool

from typing import List, Union, Dict
from pydantic import BaseModel

from db.enums import *

# -----------------------------------------------------------------
# auth classes
# -----------------------------------------------------------------

class UserBaseDTO(BaseModel):
    email: str;

class UserCreateDTO(UserBaseDTO):
    username: str;
    password: str;
    student_id: Union[str, None] = None;
    admin_id: Union[str, None] = None;
    teacher_id: Union[str, None] = None;

class UserDTO(UserBaseDTO):
    id: int;
    username: str;
    is_active: bool;

    class Config:
        orm_mode = True;

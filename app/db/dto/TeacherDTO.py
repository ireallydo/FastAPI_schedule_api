from typing import List, Union, Dict
from pydantic import BaseModel

from db.enums import *
from . import ModuleDTO

# -----------------------------------------------------------------
# teachers classes
# -----------------------------------------------------------------

class TeacherBaseDTO(BaseModel):
    pass;

class TeacherCreateDTO(TeacherBaseDTO):
    last_name: str;
    first_name: str;
    second_name: Union[str, None] = None;
    class Config:
        orm_mode = True;

class TeacherDTO(BaseModel):
    id: int;

    class Config:
        orm_mode = True;

class TeacherModulesDTO(TeacherDTO):
    modules: List[ModuleDTO];

class TeacherScheduleDTO(TeacherBaseDTO):
    last_name: str;
    first_name: str;
    second_name: Union[str, None] = None;
    class Config:
        orm_mode = True;

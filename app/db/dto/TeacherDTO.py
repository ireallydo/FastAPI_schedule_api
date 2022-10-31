from typing import List, Union, Dict, Optional
from pydantic import BaseModel

from uuid import UUID

from db.enums import ClassTypesEnum, AcademicYearsEnum, WeekdaysEnum, LessonsEnum
from db.dto import ModuleDTO


class TeacherBaseDTO(BaseModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed=True

class TeacherCreateDTO(TeacherBaseDTO):
    first_name: str
    second_name: Optional[str]
    last_name: str

class TeacherDTO(TeacherBaseDTO):
    id: UUID
    first_name: str
    second_name: Optional[str]
    last_name: str

class TeacherPatchDTO(TeacherBaseDTO):
    first_name: Optional[str]
    second_name: Optional[str]
    last_name: Optional[str]

class TeacherDeleteDTO(TeacherCreateDTO):
    pass


class TeacherModulesDTO(TeacherDTO):
    modules: List[ModuleDTO]

class TeacherScheduleDTO(TeacherBaseDTO):
    last_name: str;
    first_name: str;
    second_name: Optional[str]
    class Config:
        orm_mode = True;

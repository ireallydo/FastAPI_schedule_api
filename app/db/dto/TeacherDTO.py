from typing import List, Union, Dict, Optional
from pydantic import BaseModel, Extra
from datetime import datetime

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
    birth_date: Union[str, datetime]
    class Config:
        extra = Extra.allow

class TeacherDTO(TeacherCreateDTO):
    id: Union[UUID, str]
    registration_token: str

class TeacherProfileDTO(TeacherCreateDTO):
    id: Union[UUID, str]
    created_at: Union[str, datetime]
    updated_at: Union[str, datetime]
    deleted_at: Union[str, datetime, None]

class TeacherDeleteDTO(TeacherBaseDTO):
    deleted_at: Union[str, datetime]


class TeacherModulesDTO(TeacherDTO):
    modules: List[ModuleDTO]

class TeacherInScheduleDTO(TeacherCreateDTO):
    pass




class TeachersToModulesCreateDTO(TeacherBaseDTO):
    modules_id: List[Union[str, UUID]]

class TeachersToModulesDTO(TeacherBaseDTO):
    teacher_id: Union[str, UUID]
    modules: List[ModuleDTO]

class GetTeachersModules(TeacherBaseDTO):
    id: Union[str, UUID]

class TeachersToModulesDeleteDTO(TeachersToModulesCreateDTO):
    pass

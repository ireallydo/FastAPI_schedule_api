from typing import List, Union, Dict, Optional
from pydantic import BaseModel
from datetime import datetime

from uuid import UUID

from db.enums import ClassTypesEnum, AcademicYearsEnum


class ModuleBaseDTO(BaseModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed=True

class ModuleCreateDTO(ModuleBaseDTO):
    module_name: str
    class_type: ClassTypesEnum
    academic_year: AcademicYearsEnum

class ModuleDTO(ModuleCreateDTO):
    id: Union[UUID, str]

class PupulateTeachersDTO(ModuleBaseDTO):
    id: Union[UUID, str]
    first_name: str
    second_name: Optional[str]
    last_name: str
    birth_date: Union[str, datetime]
    deleted_at: Union[str, datetime]

class ModuleTeachersDTO(ModuleBaseDTO):
    id: Union[UUID, str]
    teachers: List[PupulateTeachersDTO]

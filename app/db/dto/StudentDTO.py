from typing import List, Union, Dict, Optional
from pydantic import BaseModel, Extra
from datetime import datetime

from uuid import UUID

from db.enums import AcademicYearsEnum, AcademicGroupsEnum


class StudentBaseDTO(BaseModel):
    class Config:
        orm_mode = True

class StudentCreateDTO(StudentBaseDTO):
    first_name: str
    second_name: Optional[str]
    last_name: str
    birth_date: Union[str, datetime]
    academic_year: AcademicYearsEnum
    academic_group: AcademicGroupsEnum
    class Config:
        extra = Extra.allow

class StudentDTO(StudentCreateDTO):
    id: Union[UUID, str]
    registration_token: str

class StudentProfileDTO(StudentCreateDTO):
    id: Union[UUID, str]
    created_at: Union[str, datetime]
    updated_at: Union[str, datetime]
    deleted_at: Union[str, datetime, None]

class StudentPatchDTO(StudentBaseDTO):
    academic_year: Optional[AcademicYearsEnum]
    academic_group: Optional[AcademicGroupsEnum]

# class StudentDeleteDTO(StudentCreateDTO):
#     pass

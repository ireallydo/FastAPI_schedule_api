from typing import List, Union, Dict, Optional
from pydantic import BaseModel

from uuid import UUID

from db.enums import AcademicYearsEnum, AcademicGroupsEnum


class StudentBaseDTO(BaseModel):
    first_name: str
    second_name: Optional[str]
    last_name: str

    class Config:
        orm_mode = True

class StudentCreateDTO(StudentBaseDTO):
    academic_year: AcademicYearsEnum
    academic_group: AcademicGroupsEnum

class StudentDTO(StudentBaseDTO):
    academic_year: AcademicYearsEnum
    academic_group: AcademicGroupsEnum
    id: UUID

class StudentPatchDTO(StudentCreateDTO):
    pass

class StudentDeleteDTO(StudentCreateDTO):
    pass

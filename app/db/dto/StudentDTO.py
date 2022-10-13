from typing import List, Union, Dict
from pydantic import BaseModel

from db.enums import *



# -----------------------------------------------------------------
# students classes
# -----------------------------------------------------------------

class StudentBaseDTO(BaseModel):
    last_name: str;
    first_name: str;
    second_name: Union[str, None] = None;

class StudentCreateDTO(StudentBaseDTO):
    academic_year: int;
    academic_group: int;

class StudentDTO(StudentBaseDTO):
    id: int;
    academic_year: int;
    academic_group: int;

    class Config:
        orm_mode = True;

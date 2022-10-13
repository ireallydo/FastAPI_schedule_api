from typing import List, Union, Dict
from pydantic import BaseModel

from db.enums import *


# -----------------------------------------------------------------
# lesson classes
# -----------------------------------------------------------------

class LessonBaseDTO(BaseModel):
    number: int;
    time: str;
    class Config:
        orm_mode = True;

class LessonCreateDTO(LessonBaseDTO):
    pass;

class LessonDTO(LessonBaseDTO):
    id: int;

class LessonScheduleDTO(LessonBaseDTO):
    pass;

from typing import List, Union, Dict, Optional
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import TIME
from uuid import UUID
from datetime import time
from db.enums import LessonsEnum


class LessonBaseDTO(BaseModel):
    class Config:
        orm_mode = True


class LessonPatchDTO(LessonBaseDTO):
    start_time: Union[str, time]
    end_time: Union[str, time]


class LessonCreateDTO(LessonPatchDTO):
    lesson_number: LessonsEnum


class LessonDTO(LessonCreateDTO):
    id: Union[UUID, str]

class LessonSearchDTO(LessonBaseDTO):
    lesson_number: LessonsEnum


class LessonDeleteDTO(LessonSearchDTO):
    pass

class LessonScheduleDTO(LessonBaseDTO):
    pass

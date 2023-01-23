from typing import List, Union, Dict, Optional
from pydantic import BaseModel

from uuid import UUID

from db.enums import LessonsEnum


class LessonBaseDTO(BaseModel):
    class Config:
        orm_mode = True

class LessonCreateDTO(LessonBaseDTO):
    lesson_number: LessonsEnum
    time: str

class LessonDTO(LessonCreateDTO):
    id: Union[UUID, str]

class LessonSearchDTO(LessonBaseDTO):
    lesson_number: LessonsEnum

class LessonPatchDTO(LessonBaseDTO):
    time: str

class LessonDeleteDTO(LessonBaseDTO):
    lesson_number: LessonsEnum

class LessonScheduleDTO(LessonBaseDTO):
    pass

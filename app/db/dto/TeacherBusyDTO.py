from typing import List, Union, Dict, Optional
from pydantic import BaseModel

from uuid import UUID

from db.enums import WeekdaysEnum, LessonsEnum

class TeacherBusyDTO(BaseModel):
    weekday: WeekdaysEnum
    lesson: LessonsEnum

    class Config:
        orm_mode = True
        arbitrary_types_allowed=True

class TeacherBusyRequestDTO(TeacherBusyDTO):
    first_name: str
    second_name: Optional[str]
    last_name: str

class TeacherBusyResponseDTO(TeacherBusyDTO):
    teacher_id: UUID
    is_busy: bool

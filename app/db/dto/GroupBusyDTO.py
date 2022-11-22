from typing import List, Union, Dict, Optional
from pydantic import BaseModel

from uuid import UUID

from db.enums import AcademicGroupsEnum, WeekdaysEnum, LessonsEnum

class GroupBusyDTO(BaseModel):
    weekday: WeekdaysEnum
    lesson_number: LessonsEnum

    class Config:
        orm_mode = True
        arbitrary_types_allowed=True

class GroupBusyRequestDTO(GroupBusyDTO):
    group_number: AcademicGroupsEnum

class GroupBusyResponseDTO(GroupBusyDTO):
    group_number: AcademicGroupsEnum
    is_busy: bool

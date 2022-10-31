from typing import List, Union, Dict, Optional
from pydantic import BaseModel

from uuid import UUID

from db.enums import LessonsEnum, WeekdaysEnum


class RoomBusyDTO(BaseModel):
    weekday: WeekdaysEnum
    lesson: LessonsEnum

    class Config:
        orm_mode = True
        arbitrary_types_allowed=True

class RoomBusyRequestDTO(RoomBusyDTO):
    room_number: int

class RoomBusyResponseDTO(RoomBusyDTO):
    room_id: UUID
    is_busy: bool

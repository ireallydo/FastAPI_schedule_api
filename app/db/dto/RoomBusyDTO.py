from typing import List, Union, Dict, Optional
from pydantic import BaseModel, Extra

from uuid import UUID

from db.enums import LessonsEnum, WeekdaysEnum


class RoomBusyDTO(BaseModel):
    weekday: WeekdaysEnum
    lesson: LessonsEnum

    class Config:
        orm_mode = True
        arbitrary_types_allowed=True

class RoomBusyRequestDTO(RoomBusyDTO):
    is_busy: bool
    class Config:
        extra = Extra.allow

class RoomBusyResponseDTO(RoomBusyRequestDTO):
    room_id: Union[UUID, str]

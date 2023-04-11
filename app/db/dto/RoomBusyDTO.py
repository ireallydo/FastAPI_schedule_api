from typing import Union
from pydantic import BaseModel
from uuid import UUID
from db.enums import LessonsEnum, WeekdaysEnum, SemestersEnum


class RoomBusyDTO(BaseModel):
    weekday: WeekdaysEnum
    lesson: LessonsEnum

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class RoomBusyRequestDTO(RoomBusyDTO):
    is_busy: bool
    semester: SemestersEnum


class RoomBusyResponseDTO(RoomBusyRequestDTO):
    room_id: Union[UUID, str]


class RoomBusyCreateDTO(RoomBusyResponseDTO):
    pass

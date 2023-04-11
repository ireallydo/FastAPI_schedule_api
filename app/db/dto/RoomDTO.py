from typing import Union
from pydantic import BaseModel
from uuid import UUID
from db.enums import ClassTypesEnum


class RoomBaseDTO(BaseModel):
    class Config:
        orm_mode = True


class RoomCreateDTO(RoomBaseDTO):
    room_number: int
    class_type: ClassTypesEnum


class RoomDTO(RoomCreateDTO):
    id: Union[UUID, str]


class RoomPatchDTO(RoomBaseDTO):
    class_type: ClassTypesEnum

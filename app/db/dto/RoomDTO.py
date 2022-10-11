from typing import List, Union, Dict
from pydantic import BaseModel

from db.enums import *


# -----------------------------------------------------------------
# rooms classes
# -----------------------------------------------------------------

class RoomBaseDTO(BaseModel):
    number: int;

class RoomCreateDTO(RoomBaseDTO):
    pass;

class RoomDTO(RoomBaseDTO):
    id: int;

    class Config:
        orm_mode = True;

class RoomBusyBaseDTO(BaseModel):
    room_id: int;
    weekday: str;
    lesson: int;
    is_busy: bool;

    class Config:
        orm_mode = True;

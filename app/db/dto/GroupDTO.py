from typing import List, Union, Dict
from pydantic import BaseModel

from db.enums import *




# -----------------------------------------------------------------
# groups classes
# -----------------------------------------------------------------

class GroupBaseDTO(BaseModel):
    number: int;

class GroupCreateDTO(GroupBaseDTO):
    pass

class GroupDTO(GroupBaseDTO):
    id: int;
    number: int;

    class Config:
        orm_mode = True;

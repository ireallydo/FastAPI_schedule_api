from typing import List, Union, Dict
from pydantic import BaseModel

from db.enums import *




# -----------------------------------------------------------------
# modules classes
# -----------------------------------------------------------------

class ModuleBaseDTO(BaseModel):
    name: str;
    class Config:
        orm_mode = True;

class ModuleCreateDTO(ModuleBaseDTO):
    year: int;

class ModuleDTO(ModuleCreateDTO):
    id: int;

class ModuleClasses(ModuleDTO):
    classes: List[ClassTypesEnum];

class ModuleScheduleDTO(ModuleBaseDTO):
    pass;

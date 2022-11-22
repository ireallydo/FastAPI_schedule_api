from typing import List, Union, Dict, Optional
from pydantic import BaseModel

from uuid import UUID

from db.enums import ClassTypesEnum, AcademicYearsEnum, WeekdaysEnum, LessonsEnum
from db.dto import ModuleDTO

class TeachersToModulesBaseDTO(BaseModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed=True

class TeachersToModulesCreateDTO(TeachersToModulesBaseDTO):
    first_name: str
    second_name: Optional[str]
    last_name: str
    module_name: str
    class_type: ClassTypesEnum

class TeachersToModulesPatchDTO(TeachersToModulesBaseDTO):
    pass

class TeachersToModulesDeleteDTO(TeachersToModulesCreateDTO):
    pass

class TeachersToModulesGetDTO(TeachersToModulesCreateDTO):
    pass

class TeachersToModulesDTO(TeachersToModulesCreateDTO):
    pass

from typing import List, Union, Dict, Optional
from pydantic import BaseModel

from uuid import UUID

from db.enums import ClassTypesEnum, AcademicYearsEnum


class ModuleBaseDTO(BaseModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed=True

class ModuleCreateDTO(ModuleBaseDTO):
    module_name: str
    class_type: ClassTypesEnum
    academic_year: AcademicYearsEnum

class ModuleDTO(ModuleBaseDTO):
    id: Union[UUID, str]
    module_name: str
    class_type: ClassTypesEnum
    academic_year: AcademicYearsEnum

class ModulePatchDTO(ModuleBaseDTO):
    module_name: Optional[str]
    class_type: Optional[ClassTypesEnum]
    academic_year: Optional[AcademicYearsEnum]

class ModuleDeleteDTO(ModuleCreateDTO):
    pass

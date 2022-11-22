from typing import List, Union, Dict, Optional
from pydantic import BaseModel

from uuid import UUID

from db.enums import ClassTypesEnum, AcademicYearsEnum, WeekdaysEnum, LessonsEnum
from db.dto import ModuleDTO

class TeachersToModulesBaseDTO(BaseModel):
    pass

class TeachersToModulesCreateDTO(TeachersToModulesBaseDTO):
    pass

class TeachersToModulesPatchDTO(TeachersToModulesBaseDTO):
    pass

class TeachersToModulesDeleteDTO(TeachersToModulesBaseDTO):
    pass

class TeachersToModulesGetDTO(TeachersToModulesBaseDTO):
    pass

class TeachersToModulesDTO(TeachersToModulesBaseDTO):
    pass

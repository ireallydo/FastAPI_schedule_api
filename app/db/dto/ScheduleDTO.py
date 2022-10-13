from typing import List, Union, Dict
from pydantic import BaseModel

from uuid import UUID

from db.enums import *
from .TeacherDTO import TeacherScheduleDTO

# -----------------------------------------------------------------
# schedule classes
# -----------------------------------------------------------------

class ScheduleBaseDTO(BaseModel):
    class Config:
        orm_mode = True;
        arbitrary_types_allowed=True

class ScheduleCreateDTO(ScheduleBaseDTO):
    pass

class ScheduleCreateManuallyDTO(ScheduleBaseDTO):
    semester: SemestersEnum;
    group_number: AcademicGroupsEnum;
    weekday: WeekdaysEnum;
    lesson_number: LessonsEnum;
    module_id: UUID;
    class_type: ClassTypesEnum;
    room_number: int;
    teacher_id: UUID;

class ScheduleDTO(ScheduleBaseDTO):
    id: UUID;
    semester: SemestersEnum;
    group_number: AcademicGroupsEnum;
    weekday: WeekdaysEnum;
    lesson_number: LessonsEnum;
    module_id: UUID;
    class_type: ClassTypesEnum;
    room_number: int;
    teacher_id: UUID;

class ScheduleGroupRequestDTO(ScheduleBaseDTO):
    semester: SemestersEnum;
    group: int;

#----------------------

class ScheduleModuleDTO(ScheduleBaseDTO):
    name: str;

class ScheduleClassDTO(ScheduleBaseDTO):
    #teacher_id: int; # for testing
    modules: ScheduleModuleDTO;
    class_type: str;
    room: int;

#-----------------------

class ScheduleClassForGroupDTO(ScheduleClassDTO):
    teachers: TeacherScheduleDTO;

class ScheduleLessonForGroupDTO(ScheduleBaseDTO):
    number: int;
    time: str;
    schedule: List[ScheduleClassForGroupDTO];

class ScheduleGroupResponseDTO(ScheduleBaseDTO):
    name: str;
    lessons: List[ScheduleLessonForGroupDTO];

#------------------------

class ScheduleClassForTeacherDTO(ScheduleClassDTO):
    group: int;

class ScheduleLessonForTeacherDTO(ScheduleBaseDTO):
    number: int;
    time: str;
    schedule: List[ScheduleClassForTeacherDTO];

class ScheduleTeacherResponseDTO(ScheduleBaseDTO):
    name: str;
    lessons: List[ScheduleLessonForTeacherDTO];

#-----------------------

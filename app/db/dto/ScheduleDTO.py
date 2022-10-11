from typing import List, Union, Dict
from pydantic import BaseModel

from db.enums import *
from .TeacherDTO import TeacherScheduleDTO

# -----------------------------------------------------------------
# schedule classes
# -----------------------------------------------------------------

class ScheduleBaseDTO(BaseModel):
    class Config:
        orm_mode = True;

class ScheduleCreateDTO(ScheduleBaseDTO):
    pass

class ScheduleCreateManuallyDTO(ScheduleBaseDTO):
    semester: SemestersEnum;
    group: int;
    weekday: WeekdaysEnum;
    lesson_number: LessonsEnum;
    module_id: int;
    class_type: ClassTypesEnum;
    room: int;
    teacher_id: int;

class ScheduleDTO(ScheduleBaseDTO):
    id: int;
    semester: int;
    group: int;
    weekday: str;
    lesson_number: int;
    module_id: int;
    class_type: str;
    room: int;
    teacher_id: int;

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

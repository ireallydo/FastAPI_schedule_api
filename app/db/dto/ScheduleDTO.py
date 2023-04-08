from typing import List, Union
from pydantic import BaseModel
from uuid import UUID
from db.enums import SemestersEnum, WeekdaysEnum, LessonsEnum, AcademicGroupsEnum, ClassTypesEnum
from .TeacherDTO import TeacherInScheduleDTO
from .LessonDTO import LessonCreateDTO
from .ModuleDTO import ModuleCreateDTO, ModuleDTO


class ScheduleBaseDTO(BaseModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ScheduleCreateDTO(ScheduleBaseDTO):
    semester: SemestersEnum
    weekday: WeekdaysEnum
    lesson_number: LessonsEnum
    group_number: AcademicGroupsEnum
    module_id: Union[str, UUID]


class ScheduleCreateManuallyDTO(ScheduleCreateDTO):
    room_number: int
    teacher_id: Union[str, UUID]


class ScheduleDTO(ScheduleBaseDTO):
    id: UUID
    semester: SemestersEnum
    group_number: AcademicGroupsEnum
    weekday: WeekdaysEnum
    lesson_number: LessonsEnum
    module_id: UUID
    class_type: ClassTypesEnum
    room_number: int
    teacher_id: UUID


class ScheduleOutDTO(ScheduleBaseDTO):
    id: Union[str, UUID]
    semester: SemestersEnum
    group_number: AcademicGroupsEnum
    weekday: WeekdaysEnum
    lesson: LessonCreateDTO
    module: ModuleCreateDTO
    room_number: int
    teacher: TeacherInScheduleDTO


class ScheduleGroupRequestDTO(ScheduleBaseDTO):
    semester: SemestersEnum
    group: int


class BusyDTO(ScheduleBaseDTO):
    is_busy: bool
    weekday: WeekdaysEnum
    lesson: LessonsEnum
    semester: SemestersEnum


class ClassesGroupDTO(ScheduleBaseDTO):
    schedule_id: Union[str, UUID]
    lesson: LessonCreateDTO
    module: ModuleDTO
    room_number: int
    teacher: TeacherInScheduleDTO


class WeekdaysGroupDTO(ScheduleBaseDTO):
    weekday: WeekdaysEnum
    classes: List[ClassesGroupDTO]


class GroupScheduleDTO(ScheduleBaseDTO):
    semester: SemestersEnum
    group_number: int
    schedule: List[WeekdaysGroupDTO]


class ClassesTeacherDTO(ScheduleBaseDTO):
    lesson: LessonCreateDTO
    module: ModuleDTO
    room_number: int
    groups: List[AcademicGroupsEnum]


class WeekdaysTeacherDTO(ScheduleBaseDTO):
    weekday: WeekdaysEnum
    classes: List[ClassesTeacherDTO]


class TeacherScheduleDTO(ScheduleBaseDTO):
    semester: SemestersEnum
    teacher: TeacherInScheduleDTO
    schedule: List[WeekdaysTeacherDTO]

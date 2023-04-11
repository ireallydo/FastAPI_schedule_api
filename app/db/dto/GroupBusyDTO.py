from pydantic import BaseModel
from db.enums import AcademicGroupsEnum, WeekdaysEnum, LessonsEnum, SemestersEnum


class GroupBusyDTO(BaseModel):
    weekday: WeekdaysEnum
    lesson: LessonsEnum

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class GroupBusyRequestDTO(GroupBusyDTO):
    is_busy: bool
    semester: SemestersEnum


class GroupBusyResponseDTO(GroupBusyRequestDTO):
    group_number: AcademicGroupsEnum


class GroupBusyCreateDTO(GroupBusyResponseDTO):
    pass

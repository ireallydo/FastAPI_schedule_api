from pydantic import BaseModel
from uuid import UUID
from db.enums import WeekdaysEnum, LessonsEnum, SemestersEnum


class TeacherBusyDTO(BaseModel):
    weekday: WeekdaysEnum
    lesson: LessonsEnum

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class TeacherBusyRequestDTO(TeacherBusyDTO):
    is_busy: bool
    semester: SemestersEnum


class TeacherBusyResponseDTO(TeacherBusyRequestDTO):
    teacher_id: UUID


class TeacherBusyCreateDTO(TeacherBusyResponseDTO):
    pass

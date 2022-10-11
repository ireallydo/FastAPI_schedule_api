from sqlalchemy import Column, ForeignKey, Unicode, DateTime, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID, BOOLEAN, INTEGER
from uuid import uuid4
from sqlalchemy.orm import relationship

from db.models import BaseModel

from db.enums import WeekdaysEnum, LessonsEnum

class TeacherBusyModel(BaseModel):
    __tablename__ = 'tbl_teachers_busy';

    teacher_id = Column('teacher_id', UUID(as_uuid=True), ForeignKey('tbl_teachers.id', ondelete="CASCADE"), primary_key=True)
    weekday = Column('weekday', Enum(WeekdaysEnum), nullable=False)
    lesson = Column('lesson', Enum(LessonsEnum), ForeignKey('tbl_lessons.lesson_number'), nullable=False)
    is_busy = Column('is_busy', Boolean, default=False)

    # many-to-one, this one is parent
    lessons = relationship('LessonModel')

from sqlalchemy import Column, ForeignKey, Unicode, DateTime, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID, BOOLEAN, INTEGER
from uuid import uuid4
from sqlalchemy.orm import relationship

from db.models import BaseModel

from db.enums import AcademicGroupsEnum, WeekdaysEnum, LessonsEnum


class GroupBusyModel(BaseModel):
    __tablename__ = 'tbl_groups_busy'

    group_number = Column('group_number', Enum(AcademicGroupsEnum), primary_key=True)
    weekday = Column('weekday', Enum(WeekdaysEnum), primary_key=True)
    lesson_number = Column('lesson_number', ForeignKey('tbl_lessons.lesson_number'), Enum(LessonsEnum), primary_key=True)
    is_busy = Column('is_busy', Boolean, default=False)

    # many-to-one, this one is parent
    lessons = relationship('LessonModel')

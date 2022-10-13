from sqlalchemy import Column, ForeignKey, Unicode, DateTime, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID, BOOLEAN, INTEGER
from uuid import uuid4
from sqlalchemy.orm import relationship

from db.models import BaseModel

from db.enums import LessonsEnum

class LessonModel(BaseModel):
    __tablename__ = 'tbl_lessons';

    lesson_number = Column('lesson_number', Enum(LessonsEnum), primary_key=True)
    time = Column('time', Unicode(255), nullable=False, unique=True)

    schedule = relationship('ScheduleModel', back_populates = 'lessons');

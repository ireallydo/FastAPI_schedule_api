from sqlalchemy import Column, ForeignKey, Unicode, DateTime, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID, BOOLEAN, INTEGER
from uuid import uuid4
from sqlalchemy.orm import relationship

from db.models import BaseModel

from db.enums import LessonsEnum

class LessonModel(BaseModel):
    __tablename__ = 'tbl_lessons';

    id = Column("id", UUID(as_uuid=True), unique=True, primary_key=True, default=uuid4)
    lesson_number = Column('lesson_number', Enum(LessonsEnum), nullable=False, unique=True)
    time = Column('time', Unicode(255), nullable=False, unique=True)

    schedule = relationship('ScheduleModel', back_populates = 'lessons');

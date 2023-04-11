from sqlalchemy import Column, Enum
from sqlalchemy.dialects.postgresql import UUID, TIME
from uuid import uuid4
from sqlalchemy.orm import relationship
from db.models import BaseModel
from db.enums import LessonsEnum


class LessonModel(BaseModel):
    __tablename__ = 'tbl_lessons'
    id = Column("id", UUID(as_uuid=True), unique=True, primary_key=True, default=uuid4)
    lesson_number = Column('lesson_number', Enum(LessonsEnum), nullable=False, unique=True)
    start_time = Column('start_time', TIME, nullable=False, unique=True)
    end_time = Column('end_time', TIME, nullable=False, unique=True)

    schedule = relationship('ScheduleModel',
                            back_populates='lessons',
                            lazy='subquery')

    def dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

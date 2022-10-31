from sqlalchemy import Column, ForeignKey, Unicode, DateTime, Enum, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID, BOOLEAN, INTEGER
from uuid import uuid4
from sqlalchemy.orm import relationship

from db.models import BaseModel, teachers_to_modules_association_table

from db.enums import WeekdaysEnum, LessonsEnum


class RoomBusyModel(BaseModel):
    __tablename__ = 'tbl_rooms_busy';

    room_id = Column('room_id', UUID(as_uuid=True), ForeignKey('tbl_rooms.id', ondelete="CASCADE"), primary_key=True)
    weekday = Column('weekday', Enum(WeekdaysEnum), primary_key=True)
    lesson = Column('lesson', Enum(LessonsEnum), ForeignKey('tbl_lessons.lesson_number'), primary_key=True)
    is_busy = Column('is_busy', Boolean, default=False)

    # many-to-one, this one is parent
    lessons = relationship('LessonModel')

from sqlalchemy import Column, func, ForeignKey, Unicode, DateTime, Enum, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID, BOOLEAN, INTEGER
from datetime import datetime
from uuid import uuid4
from sqlalchemy.orm import relationship

from db.models import BaseModel

from db.enums import LessonsEnum, WeekdaysEnum, SemestersEnum, AcademicGroupsEnum, ClassTypesEnum

class ScheduleModel(BaseModel):
    __tablename__ = 'schedule';

    id = Column("id", UUID(as_uuid=True), unique=True, primary_key=True, default=uuid4)
    semester = Column('semester', Enum(SemestersEnum))
    group_number = Column('group_number', Enum(AcademicGroupsEnum))
    weekday = Column('weekday', Enum(WeekdaysEnum))
    lesson_number = Column('lesson_number', Enum(LessonsEnum), ForeignKey('tbl_lessons.lesson_number'), nullable=False)
    module_id = Column('module_id', UUID(as_uuid=True), ForeignKey('tbl_modules.id'))
    class_type = Column('class_type', Enum(ClassTypesEnum))
    room_number = Column('room_number', Integer,  ForeignKey('tbl_rooms.room_number'))
    teacher_id = Column('teacher_id', UUID(as_uuid=True), ForeignKey('tbl_teachers.id'))

    created_at = Column('created_at', DateTime, default=datetime.utcnow)
    updated_at = Column('updated_at', DateTime, default=datetime.utcnow, onupdate=func.current_timestamp())

    lessons = relationship('LessonModel', back_populates = 'schedule');
    modules = relationship('ModuleModel', back_populates = 'schedule');
    rooms = relationship('RoomModel', back_populates = 'schedule');
    teachers = relationship('TeacherModel', back_populates = 'schedule');

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.models import BaseModel

class ScheduleModel(BaseModel):
    __tablename__ = 'schedule';

    id = Column(Integer, primary_key=True, index=True);
    semester = Column(Integer, index=True);
    group = Column(Integer, index=True);
    weekday = Column(String(255), nullable=False, index=True);
    lesson_number = Column(Integer, ForeignKey('tbl_lessons.number'), nullable=False, index=True);
    module_id = Column(Integer, ForeignKey('tbl_modules.id'), index=True);
    class_type = Column(String(255),index=True);
    room = Column(Integer, ForeignKey('tbl_rooms.number'), index=True);
    teacher_id = Column(Integer, ForeignKey('tbl_teachers.id'), nullable=False, index=True);

    lessons = relationship('Lesson', back_populates = 'schedule');
    modules = relationship('Module', back_populates = 'schedule');
    rooms = relationship('Room', back_populates = 'schedule');
    teachers = relationship('Teacher', back_populates = 'schedule');

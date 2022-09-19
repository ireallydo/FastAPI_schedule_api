from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db import Base

class ScheduleModel(Base):
    __tablename__ = 'schedule';

    id = Column(Integer, primary_key=True, index=True);
    semester = Column(Integer, index=True);
    group = Column(Integer, ForeignKey('groups.number'), index=True);
    weekday = Column(String(255), ForeignKey('weekdays.name'), nullable=False, index=True);
    lesson_number = Column(Integer, ForeignKey('lessons.number'), nullable=False, index=True);
    module_id = Column(Integer, ForeignKey('modules.id'), index=True);
    class_type = Column(String(255), ForeignKey('class_types.name'),index=True);
    room = Column(Integer, ForeignKey('rooms.number'), index=True);
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False, index=True);

    groups = relationship('AcademicGroup', back_populates = 'schedule');
    weekdays = relationship('Weekday', back_populates = 'schedule');
    lessons = relationship('Lesson', back_populates = 'schedule');
    modules = relationship('Module', back_populates = 'schedule');
    class_types = relationship('TypeOfClass', back_populates = 'schedule');
    rooms = relationship('Room', back_populates = 'schedule');
    teachers = relationship('Teacher', back_populates = 'schedule');

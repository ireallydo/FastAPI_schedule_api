from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models import weekdays_to_lessons

from db import Base

class WeekdayModel(Base):
    __tablename__ = 'weekdays';

    id = Column(Integer, primary_key=True, index=True);
    name = Column(String(255), nullable=False, unique=True, index=True);

    lessons = relationship('LessonModel',
                           order_by = 'asc(Lesson.id)',
                           secondary = weekdays_to_lessons,
                           #overlaps='weekdays',
                           back_populates='weekdays');

    schedule = relationship('ScheduleModel', back_populates = 'weekdays');

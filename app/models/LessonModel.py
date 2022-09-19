from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models import weekdays_to_lessons

from db import Base

class LessonModel(Base):
    __tablename__ = 'lessons';

    id = Column(Integer, primary_key=True, index=True);
    number = Column(Integer, nullable=False, unique=True, index=True);
    time = Column(String(255), nullable=False, unique=True, index=True);

    weekdays = relationship('WeekdayModel',
                            secondary = weekdays_to_lessons,
                            #overlaps='lessons',
                            back_populates='lessons');

    schedule = relationship('ScheduleModel', back_populates = 'lessons');

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.models import BaseModel

class LessonModel(BaseModel):
    __tablename__ = 'tbl_lessons';

    id = Column(Integer, primary_key=True, index=True);
    number = Column(Integer, nullable=False, unique=True, index=True);
    time = Column(String(255), nullable=False, unique=True, index=True);

    schedule = relationship('ScheduleModel', back_populates = 'lessons');

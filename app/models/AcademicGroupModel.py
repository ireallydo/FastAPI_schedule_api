from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from db import Base

class AcademicGroupModel(Base):
    __tablename__ = 'groups';

    id = Column(Integer, primary_key=True, index=True);
    number = Column(Integer, primary_key=True, index=True);
    # students - groups - many-to-one

    students = relationship('StudentModel', back_populates = 'group');
    schedule = relationship('ScheduleModel', back_populates = 'groups');

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models import teachers_to_modules

from db import Base

class TeacherModel(Base):
    __tablename__ = 'teachers';

    id = Column(Integer, primary_key=True, index=True);
    last_name = Column(String(255), nullable=False, index=True);
    first_name = Column(String(255), nullable=False, index=True);
    second_name = Column(String(255), index=True);

    modules = relationship('ModuleModel',
                           order_by = 'asc(Module.name)',
                           secondary = teachers_to_modules,
                           #overlaps = 'teachers',
                           back_populates='teachers');

    username = relationship('UserModel', back_populates = 'teacher', uselist = False);
    schedule = relationship('ScheduleModel', back_populates = 'teachers');

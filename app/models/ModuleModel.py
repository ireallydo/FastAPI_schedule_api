from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models import modules_to_typesOfClasses, teachers_to_modules

from db import Base

class ModuleModel(Base):
    __tablename__ = 'modules';

    id = Column(Integer, primary_key=True, index=True);
    name = Column(String(255), nullable=False, index=True);
    year = Column(Integer, nullable=False, index=True);

    classes = relationship('TypeOfClassModel',
                           order_by = 'asc(TypeOfClass.id)',
                           secondary = modules_to_typesOfClasses,
                           #overlaps='modules',
                           back_populates='modules');

    teachers = relationship('TeacherModel',
                           order_by = 'asc(Teacher.last_name)',
                           secondary = teachers_to_modules,
                           #overlaps = 'modules',
                           back_populates='modules');

    schedule = relationship('ScheduleModel', back_populates = 'modules');

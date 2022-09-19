from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models import modules_to_typesOfClasses

from db import Base

class TypeOfClassModel(Base):
    __tablename__ = 'class_types';

    id = Column(Integer, primary_key=True, index=True);
    name = Column(String(255), nullable=False, index=True);

    modules = relationship('ModuleModel',
                           order_by = 'asc(Module.name)',
                           secondary = modules_to_typesOfClasses,
                           #overlaps='classes',
                           back_populates='classes');

    # class_type - rooms - one-to-many
    rooms = relationship('RoomModel', back_populates = 'class_type');

    # class_type - schedule - one-to-many
    schedule = relationship('ScheduleModel', back_populates = 'class_types');

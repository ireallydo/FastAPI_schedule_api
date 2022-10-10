from sqlalchemy import Column, ForeignKey, Unicode, DateTime, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID, BOOLEAN, INTEGER
from uuid import uuid4
from sqlalchemy.orm import relationship

from models import teachers_to_modules_association_table

from db.models import BaseModel

from enums import ClassTypesEnum

class RoomModel(BaseModel):
    __tablename__ = 'tbl_rooms';

    id = Column('id', Integer, primary_key=True)
    room_number = Column('room_number', Integer, primary_key=True)
    class_type = Column('class_type', Enum(ClassTypesEnum))

    schedule = relationship('ScheduleModel', back_populates='rooms');

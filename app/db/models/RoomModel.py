from sqlalchemy import Column, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from sqlalchemy.orm import relationship
from db.models import BaseModel, teachers_to_modules_association_table
from db.enums import ClassTypesEnum


class RoomModel(BaseModel):
    __tablename__ = 'tbl_rooms'
    id = Column("id", UUID(as_uuid=True), unique=True, primary_key=True, default=uuid4)
    room_number = Column('room_number', Integer, unique=True)
    class_type = Column('class_type', Enum(ClassTypesEnum))

    schedule = relationship('ScheduleModel',
                            back_populates='rooms',
                            lazy='subquery')

    def dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

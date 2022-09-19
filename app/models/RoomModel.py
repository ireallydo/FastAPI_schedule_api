from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db import Base

class RoomModel(Base):
    __tablename__ = 'rooms';

    id = Column(Integer, primary_key=True, index=True);
    number = Column(Integer, primary_key=True, index=True);
    class_type_id = Column(Integer, ForeignKey('class_types.id'), index=True);
    # class_type - rooms - one-to-many
    # rooms - schedule - one-to-many

    class_type = relationship('TypeOfClassModel', back_populates = 'rooms');
    schedule = relationship('ScheduleModel', back_populates = 'rooms');

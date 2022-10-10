from sqlalchemy import Boolean, Column, Integer, String

from db import Base

class RoomBusyModel(Base):
    __tablename__ = 'rooms_busy';

    id = Column(Integer, primary_key=True, index=True);
    room_id = Column(Integer, nullable=False, index=True);
    weekday = Column(String(255), nullable=False, index=True);
    lesson = Column(Integer, nullable=False, index=True);
    is_busy = Column(Boolean, index=True, default=False, nullable=False);

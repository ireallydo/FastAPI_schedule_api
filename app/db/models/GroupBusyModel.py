from sqlalchemy import Boolean, Column, Integer, String

from db import Base

class GroupBusyModel(Base):
    __tablename__ = 'groups_busy';

    id = Column(Integer, primary_key=True, index=True);
    group_id = Column(Integer, nullable=False, index=True);
    weekday = Column(String(255), nullable=False, index=True);
    lesson = Column(Integer, nullable=False, index=True);
    is_busy = Column(Boolean, index=True, default=False);

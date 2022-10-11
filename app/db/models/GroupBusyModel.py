from sqlalchemy import Boolean, Column, Integer, String

from db.models import BaseModel

class GroupBusyModel(BaseModel):
    __tablename__ = 'tbl_groups_busy'

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, nullable=False)
    weekday = Column(String(255), nullable=False)
    lesson = Column(Integer, nullable=False)
    is_busy = Column(Boolean, default=False)

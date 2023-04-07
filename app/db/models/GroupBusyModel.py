from sqlalchemy import Column, ForeignKey, Unicode, DateTime, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID, BOOLEAN, INTEGER
from uuid import uuid4
from sqlalchemy.orm import relationship

from db.models import BaseModel

from db.enums import AcademicGroupsEnum, WeekdaysEnum, LessonsEnum, SemestersEnum


class GroupBusyModel(BaseModel):
    __tablename__ = 'tbl_groups_busy'
    group_number = Column('group_number', Enum(AcademicGroupsEnum), primary_key=True)
    semester = Column('semester', Enum(SemestersEnum))
    weekday = Column('weekday', Enum(WeekdaysEnum), primary_key=True)
    lesson = Column('lesson', Enum(LessonsEnum), primary_key=True)
    is_busy = Column('is_busy', Boolean, default=False)

    def dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
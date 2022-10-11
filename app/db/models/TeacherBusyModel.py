from sqlalchemy import Boolean, Column, Integer, String

from db.models import BaseModel

class TeacherBusyModel(Base):
    __tablename__ = 'tbl_teachers_busy';

    id = Column(Integer, primary_key=True, index=True);
    teacher_id = Column(Integer, nullable=False, index=True);
    weekday = Column(String(255), nullable=False, index=True);
    lesson = Column(Integer, nullable=False, index=True);
    is_busy = Column(Boolean, index=True, default=False);

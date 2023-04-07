from sqlalchemy import Column, ForeignKey, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.models import BaseModel
from db.enums import WeekdaysEnum, LessonsEnum, SemestersEnum

class TeacherBusyModel(BaseModel):
    __tablename__ = 'tbl_teachers_busy';
    teacher_id = Column('teacher_id', UUID(as_uuid=True), ForeignKey('tbl_teachers.id', ondelete="CASCADE"), primary_key=True)
    semester = Column('semester', Enum(SemestersEnum))
    weekday = Column('weekday', Enum(WeekdaysEnum), nullable=False, primary_key=True)
    lesson = Column('lesson', Enum(LessonsEnum), ForeignKey('tbl_lessons.lesson_number'), nullable=False, primary_key=True)
    is_busy = Column('is_busy', Boolean, default=False)

    #many-to-one, this one is parent
    lessons = relationship('LessonModel')

    def dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
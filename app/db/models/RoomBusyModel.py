from sqlalchemy import Column, ForeignKey, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.models import BaseModel, teachers_to_modules_association_table
from db.enums import WeekdaysEnum, LessonsEnum, SemestersEnum


class RoomBusyModel(BaseModel):
    __tablename__ = 'tbl_rooms_busy'
    room_id = Column('room_id', UUID(as_uuid=True),
                     ForeignKey('tbl_rooms.id', ondelete="CASCADE"), primary_key=True)
    semester = Column('semester', Enum(SemestersEnum))
    weekday = Column('weekday', Enum(WeekdaysEnum), primary_key=True)
    lesson = Column('lesson', Enum(LessonsEnum),
                    ForeignKey('tbl_lessons.lesson_number'), primary_key=True)
    is_busy = Column('is_busy', Boolean, default=False)

    # many-to-one, this one is a parent
    lessons = relationship('LessonModel',
                           lazy='subquery')

    def dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

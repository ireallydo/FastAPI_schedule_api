from sqlalchemy import Column, ForeignKey
from sqlalchemy.schema import Table

from db import Base

weekdays_to_lessons = Table(
    'weekdays_to_lessons_association', Base.metadata,
    Column('Weekday_id', ForeignKey('weekdays.id')),
    Column('Lesson_id', ForeignKey('lessons.id'))
    );

from sqlalchemy import Column, ForeignKey
from sqlalchemy.schema import Table

from db import Base

teachers_to_modules = Table(
    'teachers_to_modules', Base.metadata,
    Column('Teacher_id', ForeignKey('teachers.id')),
    Column('Module_id', ForeignKey('modules.id'))
    );

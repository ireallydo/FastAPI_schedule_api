from sqlalchemy import Column, ForeignKey
from sqlalchemy.schema import Table

from db.models import BaseModel

teachers_to_modules_association_table = Table(
    'teachers_to_modules', BaseModel.metadata,
    Column('teacher_id', ForeignKey('teachers.id', ondelete="CASCADE"), primary_key=True),
    Column('module_id', ForeignKey('modules.id', ondelete="CASCADE"), primary_key=True)
    );

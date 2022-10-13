from sqlalchemy import Column, ForeignKey
from sqlalchemy.schema import Table

from db.models import BaseModel

teachers_to_modules_association = Table(
    'teachers_to_modules', BaseModel.metadata,
    Column('teacher_id', ForeignKey('tbl_teachers.id', ondelete="CASCADE"), primary_key=True),
    Column('module_id', ForeignKey('tbl_modules.id', ondelete="CASCADE"), primary_key=True)
    )

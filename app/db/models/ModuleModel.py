from sqlalchemy import Column, ForeignKey, Unicode, DateTime, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID, BOOLEAN, INTEGER
from uuid import uuid4
from sqlalchemy.orm import relationship

from models import teachers_to_modules_association_table

from db.models import BaseModel

from enums import ClassTypesEnum, AcademicYearsEnum

class ModuleModel(BaseModel):
    __tablename__ = 'tbl_modules'

    id = Column("id", UUID(as_uuid=True), unique=True, primary_key=True, default=uuid4)
    module_name = Column('module_name', Unicode(255), nullable=False)
    class_type = Column('class_type', Enum(ClassTypesEnum))
    academic_year = Column('academic_year', Enum(AcademicYearsEnum), nullable=False)

    teachers = relationship('TeacherModel',
                           order_by='asc(Teacher.last_name)',
                           secondary=teachers_to_modules_association_table,
                           back_populates='modules')

    schedule = relationship('ScheduleModel', back_populates='modules')
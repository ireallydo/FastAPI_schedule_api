from sqlalchemy import Column, ForeignKey, Unicode, DateTime, Enum, Boolean, String
from sqlalchemy.dialects.postgresql import UUID, BOOLEAN, INTEGER
from uuid import uuid4
from sqlalchemy.orm import relationship

from db.models import BaseModel
from db.models.teachers_to_modules_association_table import teachers_to_modules_association
from db.enums import ClassTypesEnum, AcademicYearsEnum


class ModuleModel(BaseModel):
    __tablename__ = 'tbl_modules'

    id = Column("id", UUID(as_uuid=True), unique=True, nullable=False, default=uuid4)
    module_name = Column('module_name', String(255), primary_key=True)
    class_type = Column('class_type', Enum(ClassTypesEnum), primary_key=True)
    academic_year = Column('academic_year', Enum(AcademicYearsEnum), primary_key=True)

    teachers = relationship('TeacherModel',
                           order_by='asc(TeacherModel.last_name)',
                           secondary=teachers_to_modules_association,
                           back_populates='modules')

    schedule = relationship('ScheduleModel', back_populates='modules')

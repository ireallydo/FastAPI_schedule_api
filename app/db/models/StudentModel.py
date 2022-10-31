from sqlalchemy import Column, func, ForeignKey, String, DateTime, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID, BOOLEAN, INTEGER
from datetime import datetime
from uuid import uuid4
from sqlalchemy.orm import relationship

from db.models import BaseModel, UserModel

from db.enums import AcademicYearsEnum, AcademicGroupsEnum

class StudentModel(BaseModel):
    __tablename__ = 'tbl_students'

    id = Column('id', UUID(as_uuid=True), unique=True, primary_key=True, default=uuid4)
    login = Column('login', String(255), ForeignKey('tbl_users.login'), unique=True, nullable=True)
    first_name = Column('first_name', String(255), nullable=False)
    second_name = Column('second_name', String(255))
    last_name = Column('last_name', String(255), nullable=False)
    academic_year = Column('academic_year', Enum(AcademicYearsEnum))
    academic_group = Column('academic_group', Enum(AcademicGroupsEnum))

    created_at = Column('created_at', DateTime, default=datetime.utcnow)
    updated_at = Column('updated_at', DateTime, default=datetime.utcnow, onupdate=func.current_timestamp())


    users = relationship('UserModel', back_populates='students', uselist=False)

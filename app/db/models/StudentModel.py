from sqlalchemy import Column, func, String, DateTime, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from uuid import uuid4
from db.models import BaseModel, UserModel
from db.enums import AcademicYearsEnum, AcademicGroupsEnum


class StudentModel(BaseModel):
    __tablename__ = 'tbl_students'
    id = Column('id', UUID(as_uuid=True), unique=True, primary_key=True, default=uuid4)
    registration_token = Column('registration_token', String(255), unique=True, nullable=False)
    registered_user = Column('registered_user', Boolean, default=False)
    first_name = Column('first_name', String(255), nullable=False)
    second_name = Column('second_name', String(255), default=None)
    last_name = Column('last_name', String(255), nullable=False)
    birth_date = Column('birth_date', DateTime, nullable=False)
    academic_year = Column('academic_year', Enum(AcademicYearsEnum))
    academic_group = Column('academic_group', Enum(AcademicGroupsEnum))
    created_at = Column('created_at', DateTime, default=datetime.utcnow)
    updated_at = Column('updated_at', DateTime, default=datetime.utcnow, onupdate=func.current_timestamp())
    deleted_at = Column('deleted_at', DateTime, default=None)

    def dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

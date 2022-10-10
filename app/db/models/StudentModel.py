from sqlalchemy import Column, ForeignKey, Unicode, DateTime, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID, BOOLEAN, INTEGER
from uuid import uuid4
from sqlalchemy.orm import relationship

from db.models import BaseModel

from enums import AcademicYearsEnum, AcademicGroupsEnum

class StudentModel(BaseModel):
    __tablename__ = 'tbl_students'

    id = Column('id', UUID(as_uuid=True), unique=True, primary_key=True, default=uuid4)
    login = Column('login', Unicode(255), unique=True, ForeignKey('tbl_users.login'), nullable=True)
    first_name = Column('first_name', Unicode(255), nullable=False)
    second_name = Column('second_name', Unicode(255))
    last_name = Column('last_name', Unicode(255), nullable=False)
    academic_year = Column('academic_year', Enum(AcademicYearsEnum))
    academic_group = Column('academic_group', Enum(AcademicGroupsEnum))

    created_at = Column('created_at', DateTime, default=datetime.utcnow)
    updated_at = Column('updated_at'. DateTime, default=datetime.utcnow, onupdate=func.current_timestamp())

    users = relationship('UserModel', back_populates='students', uselist=False);

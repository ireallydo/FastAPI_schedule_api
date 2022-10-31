from sqlalchemy import Column, func, ForeignKey, String, DateTime, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID, BOOLEAN, INTEGER
from datetime import datetime
from uuid import uuid4
from sqlalchemy.orm import relationship

from db.models import BaseModel, TeacherModel, StudentModel

from db.enums import UserRolesEnum

class UserModel(BaseModel):
    __tablename__ = 'tbl_users'

    id = Column('id', UUID(as_uuid=True), unique=True, primary_key=True, default=uuid4)
    login = Column('login', String(255), unique=True)
    email = Column('email', String(255), unique=True)
    password = Column('password',  String(255))
    user_role = Column('user_role', Enum(UserRolesEnum))
    is_active = Column('is_active', Boolean, default=True)

    created_at = Column('created_at', DateTime, default=datetime.utcnow)
    updated_at = Column('updated_at', DateTime, default=datetime.utcnow, onupdate=func.current_timestamp())

    students = relationship('StudentModel', back_populates='users');
    teachers = relationship('TeacherModel', back_populates='users');

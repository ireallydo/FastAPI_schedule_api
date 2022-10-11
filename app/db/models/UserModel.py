from sqlalchemy import Column, func, ForeignKey, Unicode, DateTime, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID, BOOLEAN, INTEGER
from datetime import datetime
from uuid import uuid4
from sqlalchemy.orm import relationship

from db.models import BaseModel

from db.enums import UserRolesEnum

class UserModel(BaseModel):
    __tablename__ = 'tbl_users'

    id = Column('id', UUID(as_uuid=True), unique=True, primary_key=True, default=uuid4)
    login = Column('login', Unicode(255), unique=True)
    email = Column('email', Unicode(255), unique=True)
    hashed_password = Column('hashed_password',  Unicode(255))
    is_active = Column('is_active', Boolean, default=True)
    #user_role = Column('role', Enum(UserRolesEnum), nullable=False)

    created_at = Column('created_at', DateTime, default=datetime.utcnow)
    updated_at = Column('updated_at', DateTime, default=datetime.utcnow, onupdate=func.current_timestamp())

    students = relationship('StudentModel', back_populates='users');
    teachers = relationship('TeacherModel', back_populates='users');

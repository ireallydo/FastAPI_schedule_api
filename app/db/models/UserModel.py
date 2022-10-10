from sqlalchemy import Column, ForeignKey, Unicode, DateTime, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID, BOOLEAN, INTEGER
from uuid import uuid4
from sqlalchemy.orm import relationship

from db.models import BaseModel

from enums import UserRolesEnum

class UserModel(BaseModel):
    __tablename__ = 'tbl_users'

    id = Column('id', UUID(as_uuid=True), unique=True, primary_key=True, default=uuid4)
    login = Column('login', Unicode(255), unique=True)
    email = Column('email', Unicode(255), unique=True)
    hashed_password = Column('hashed_password',  Unicode(255))
    is_active = Column('is_active', Boolean, default=True)
    role = Column('role', Enum(UserRolesEnum))

    created_at = Column('created_at', DateTime, default=datetime.utcnow)
    updated_at = Column('updated_at'. DateTime, default=datetime.utcnow, onupdate=func.current_timestamp())

    students = relationship('StudentModel', back_populates='users');
    teachers = relationship('TeacherModel', back_populates='users');

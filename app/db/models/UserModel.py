from sqlalchemy import Column, func, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from uuid import uuid4
from db.models import BaseModel, TeacherModel, StudentModel


class UserModel(BaseModel):
    __tablename__ = 'tbl_users'
    id = Column('id', UUID(as_uuid=True), unique=True, primary_key=True, default=uuid4)
    login = Column('login', String(255), unique=True)
    email = Column('email', String(255), unique=True)
    password = Column('password',  String(255))
    role = Column('role', String(255))
    blocked = Column('blocked', Boolean, default=False)
    is_active = Column('is_active', Boolean, default=True)
    created_at = Column('created_at', DateTime, default=datetime.utcnow)
    updated_at = Column('updated_at', DateTime, default=datetime.utcnow, onupdate=func.current_timestamp())

    def dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


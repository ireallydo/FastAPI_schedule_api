from sqlalchemy import Column, func, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from uuid import uuid4
from db.models import BaseModel, UserModel


class SessionModel(BaseModel):
    __tablename__ = 'tbl_sessions'
    id = Column('id', UUID(as_uuid=True), unique=True, primary_key=True, default=uuid4)
    user_id = Column('user_id', UUID(as_uuid=True))
    login = Column('login', String(255))
    role = Column('role', String(255))
    access_token = Column('access_token', String(255))
    access_expire_time = Column('access_expire_time', DateTime)
    refresh_token = Column('refresh_token', String(255))
    refresh_expire_time = Column('refresh_expire_time', DateTime)
    created_at = Column('created_at', DateTime, default=datetime.utcnow)
    updated_at = Column('updated_at', DateTime, default=datetime.utcnow, onupdate=func.current_timestamp())

    def dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

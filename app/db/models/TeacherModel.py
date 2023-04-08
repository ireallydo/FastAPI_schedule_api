from sqlalchemy import Column, func, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from uuid import uuid4
from sqlalchemy.orm import relationship
from db.models import BaseModel, ModuleModel, UserModel, ScheduleModel
from db.models.teachers_to_modules_association_table import teachers_to_modules_association


class TeacherModel(BaseModel):
    __tablename__ = 'tbl_teachers'
    id = Column('id', UUID(as_uuid=True), unique=True, primary_key=True, default=uuid4)
    registration_token = Column('registration_token', String(255), unique=True, nullable=False)
    registered_user = Column('registered_user', Boolean, default=False)
    first_name = Column('first_name', String(255), nullable=False)
    second_name = Column('second_name', String(255), default=None)
    last_name = Column('last_name', String(255), nullable=False)
    birth_date = Column('birth_date', DateTime, nullable=False)
    created_at = Column('created_at', DateTime, default=datetime.utcnow)
    updated_at = Column('updated_at', DateTime, default=datetime.utcnow, onupdate=func.current_timestamp())
    deleted_at = Column('deleted_at', DateTime, default=None)

    modules = relationship('ModuleModel',
                           order_by='asc(ModuleModel.module_name)',
                           secondary=teachers_to_modules_association,
                           back_populates='teachers',
                           lazy='subquery')

    def dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

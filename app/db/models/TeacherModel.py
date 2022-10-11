from sqlalchemy import Column, func, ForeignKey, Unicode, DateTime, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID, BOOLEAN, INTEGER
from datetime import datetime
from uuid import uuid4
from sqlalchemy.orm import relationship

from db.models import BaseModel, teachers_to_modules_association_table

class TeacherModel(BaseModel):
    __tablename__ = 'tbl_teachers'

    id = Column('id', UUID(as_uuid=True), unique=True, primary_key=True, default=uuid4)
    login = Column('login', Unicode(255), ForeignKey('tbl_users.login'), unique=True, nullable=True)
    first_name = Column('first_name', Unicode(255), nullable=False)
    second_name = Column('second_name', Unicode(255))
    last_name = Column('last_name', Unicode(255), nullable=False)

    created_at = Column('created_at', DateTime, default=datetime.utcnow)
    updated_at = Column('updated_at', DateTime, default=datetime.utcnow, onupdate=func.current_timestamp())

    modules = relationship('ModuleModel',
                           order_by='asc(Module.module_name)',
                           secondary=teachers_to_modules_association_table,
                           back_populates='teachers')

    users = relationship('UserModel', back_populates='teachers', uselist=False);
    schedule = relationship('ScheduleModel', back_populates='teachers')

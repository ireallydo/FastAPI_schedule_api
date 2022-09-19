from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db import Base

class UserModel(Base):
    ''' '''
    __tablename__ = 'users';

    test_col = Column(Integer);
    new_col = Column(Integer);
    id = Column(Integer, primary_key=True, index=True);
    username = Column(String(255), unique=True, index=True);
    email = Column(String(255), unique=True, index=True);
    hashed_password = Column(String(255));
    is_active = Column(Boolean, default=True);
    student_id = Column(Integer, ForeignKey('students.id'), unique=True, index=True);
    admin_id = Column(Integer, ForeignKey('admins.id'), unique=True, index=True);
    teacher_id = Column(Integer, ForeignKey('teachers.id'), unique=True, index=True);
    # users - students - one-to-one (unique)
    # users - teachers - one-to-one (unique)
    # users - administration - one-to-one (unique)

    student = relationship('StudentModel', back_populates='username');
    admin = relationship('Admin', back_populates='username');
    teacher = relationship('TeacherModel', back_populates='username');

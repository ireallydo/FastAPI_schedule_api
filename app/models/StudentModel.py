from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db import Base

class StudentModel(Base):
    __tablename__ = 'students';

    id = Column(Integer, primary_key=True, index=True);
    last_name = Column(String(255), nullable=False, index=True);
    first_name = Column(String(255), nullable=False, index=True);
    second_name = Column(String(255), index=True);
    academic_year = Column(Integer, ForeignKey('years.number'), index=True);
    academic_group = Column(Integer, ForeignKey('groups.number'), index=True);
    # students - years - many-to-one
    # students - groups - many-to-one
    # users - students - one-to-one (unique)

    year = relationship('AcademicYearModel', back_populates='students');
    group = relationship('AcademicGroupModel', back_populates='students');
    username = relationship('UserModel', back_populates='student', uselist=False);
